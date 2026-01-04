#Real QIE on-chain logic

import streamlit as st
import json
from datetime import datetime
from web3 import Web3, HTTPProvider
import os
from dotenv import load_dotenv
# from eth_utils import to_bytes


# ===============================
# Load environment variables
# ===============================
load_dotenv()

RPC_URL = os.getenv("QIE_RPC_URL")
PRIVATE_KEY = os.getenv("QIE_PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
DEPLOYER_WALLET = os.getenv("DEPLOYER_WALLET")

# ===============================
# Streamlit page config
# ===============================
st.set_page_config(
    page_title="FraudGuard Labs",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ FraudGuard Labs – AI Blockchain Fraud Detection")
st.info("💡 Demo Mode – No real user funds are affected")
st.warning("⚠️ Private keys are loaded securely via environment variables")

# ===============================
# Web3 initialization
# ===============================
w3 = Web3(Web3.HTTPProvider(RPC_URL))
w3.eth.default_account = DEPLOYER_WALLET

if w3.eth.chain_id != 1983: # type: ignore
    st.error("Wrong network! Connect to QIE Testnet (chainId 1983).")
    st.stop()

if w3.is_connected():
    st.success("Connected to QIE Testnet ✅")
else:
    st.error("Failed to connect to QIE Testnet ❌")
    st.stop()

# ===============================
# Load contract ABI
# ===============================
with open("contract_abi.json", "r") as f:
    CONTRACT_ABI = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=CONTRACT_ABI
)

# ===============================
# Blockchain interaction helpers
# ===============================
def get_nonce():
    return w3.eth.get_transaction_count(
        w3.eth.default_account,
        "pending"
    )

def freeze_wallet_on_chain(wallet_address, tx_id_hex, risk_score):
    try:
        tx_id_bytes32 = bytes.fromhex(tx_id_hex[2:])
        if len(tx_id_bytes32) != 32:
            raise ValueError("Transaction ID must be 32 bytes")

        tx = contract.functions.logFraud(
            tx_id_bytes32,
            int(risk_score),
            Web3.to_checksum_address(wallet_address)
        ).build_transaction({
            "from": w3.eth.default_account,
            "nonce": get_nonce(),
            "gas": 200000,
            "gasPrice": w3.eth.gas_price
        })

        signed_tx = w3.eth.account.sign_transaction(
            tx,
            private_key=PRIVATE_KEY
        )

        tx_hash = w3.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash.hex()

    except Exception as e:
        st.error(f"Freeze failed: {e}")
        return None


def unfreeze_wallet_on_chain(wallet_address):
    try:
        tx = contract.functions.unfreezeWallet(
            Web3.to_checksum_address(wallet_address)
        ).build_transaction({
            "from": w3.eth.default_account,
            "nonce": get_nonce(),
            "gas": 100000,
            "gasPrice": w3.eth.gas_price
        })

        signed_tx = w3.eth.account.sign_transaction(
            tx,
            private_key=PRIVATE_KEY
        )

        tx_hash = w3.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash.hex()

    except Exception as e:
        st.error(f"Unfreeze failed: {e}")
        return None


def is_wallet_frozen_on_chain(wallet_address):
    try:
        return contract.functions.isWalletFrozen(
            Web3.to_checksum_address(wallet_address)
        ).call()
    except Exception as e:
        st.error(f"Status check failed: {e}")
        return False

# ===============================
# Load AI model
# ===============================
from ai.inference import FraudDetectionAI

@st.cache_resource
def load_ai_model():
    return FraudDetectionAI()

ai_model = load_ai_model()

# ===============================
# Session state
# ===============================
if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "frozen_wallets" not in st.session_state:
    st.session_state.frozen_wallets = {}

# ===============================
# Sidebar
# ===============================
with st.sidebar:
    st.header("📜 Contract Info")
    st.code(CONTRACT_ADDRESS)
    st.metric("Transactions Analyzed", len(st.session_state.transactions))
    st.metric("Wallets Frozen", len(st.session_state.frozen_wallets))
    risk_threshold = st.slider("Risk Threshold", 1, 100, 80)
    st.divider()
    demo_high_risk = st.checkbox("🔥 Demo High-Risk Mode (Judges)")
    
    # Risk Legend
    st.markdown("### Risk Legend")
    st.markdown("🟢 Low < 50  |  🟠 Medium 50–79  |  🔴 High ≥ 80")

# ===============================
# Transaction analysis
# ===============================
st.header("🔍 Transaction Analysis")

with st.form("tx_form"):
    wallet_input = st.text_input("Wallet Address", placeholder="0x...")
    amount = st.number_input(
        "Transaction Amount (USD)",
        min_value=0.0,
        max_value=1_000_000.0,
        value=1000.0,
        step=10.0
    )
    recent_count = st.number_input(
        "Recent Transaction Count",
        min_value=0,
        max_value=100,
        value=3
    )
    suspicious_time = st.checkbox("Transaction at suspicious time?")
    submitted = st.form_submit_button("Analyze Transaction")

if submitted:
    if not Web3.is_address(wallet_input):
        st.error("Invalid wallet address")
    else:
        ai_result = ai_model.predict_fraud({
            "amount": amount,
            "wallet_address": wallet_input,
            "timestamp": int(datetime.now().timestamp()),
            "recent_transactions": list(range(recent_count)),  # Simulated recent transaction history for demo purposes
            "suspicious_time": suspicious_time
        })

        risk_score = ai_result["risk_score"]
        reason = ai_result.get("reason", "Suspicious activity detected")
        if demo_high_risk:
            risk_score = 95
            reason = "Demo Mode: Simulated high-risk fraud pattern"


        raw_tx_id = ai_result["transaction_id"][:64]
        tx_id_hex = "0x" + raw_tx_id.ljust(64, "0")

        tx_hash = None
        if risk_score >= risk_threshold:
            tx_hash = freeze_wallet_on_chain(
                wallet_input,
                tx_id_hex,
                risk_score
            )
            if tx_hash:
                st.session_state.frozen_wallets[wallet_input] = tx_hash

        st.session_state.transactions.append({
            "wallet": wallet_input,
            "amount": amount,
            "risk_score": risk_score,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "tx_hash": tx_hash
        })

        # ----- Risk Visualization -----
        if risk_score >= risk_threshold:
            st.error(f"🔴 HIGH FRAUD RISK ({risk_score})")
        elif risk_score >= 50:
            st.warning(f"🟠 MEDIUM FRAUD RISK ({risk_score})")
        else:
            st.success(f"🟢 LOW FRAUD RISK ({risk_score})")

        st.progress(min(risk_score / 100, 1.0))

        if tx_hash:
            st.code(f"🔗 Freeze TX Hash: {tx_hash}")


# ===============================
# Wallet status check
# ===============================
st.header("🔐 Wallet Status Check")

check_wallet = st.text_input("Wallet to check", placeholder="0x...")
if st.button("Check Status"):
    if Web3.is_address(check_wallet):
        frozen = is_wallet_frozen_on_chain(check_wallet)
        if frozen:
            st.error("⚠️ Wallet is FROZEN on-chain")
        else:
            st.success("✅ Wallet is ACTIVE")
    else:
        st.error("Invalid wallet address")

# ===============================
# Admin – Frozen wallets
# ===============================
if st.session_state.frozen_wallets:
    st.header("🛑 Frozen Wallets (Admin)")

    table_data = [
        {"Wallet": w, "TX Hash": h}
        for w, h in st.session_state.frozen_wallets.items()
    ]
    st.table(table_data)

    selected_wallet = st.selectbox(
        "Select wallet to unfreeze",
        list(st.session_state.frozen_wallets.keys())
    )

    if st.button("Unfreeze Wallet"):
        tx_hash = unfreeze_wallet_on_chain(selected_wallet)
        if tx_hash:
            st.session_state.frozen_wallets.pop(selected_wallet)
            st.success(f"Wallet unfrozen | TX: {tx_hash}")

# ===============================
# Transaction history
# ===============================
st.header("📜 Transaction History (Last 5)")

for tx in st.session_state.transactions[-5:]:
    level = (
        "HIGH" if tx["risk_score"] >= risk_threshold
        else "MEDIUM" if tx["risk_score"] >= 50
        else "LOW"
    )

    st.markdown(
        f"""
        **Wallet:** `{tx['wallet']}`  
        **Amount:** ${tx['amount']:,}  
        **Risk Score:** {tx['risk_score']} ({level})  
        **Reason:** {tx['reason']}  
        **Timestamp:** {tx['timestamp']}  
        **TX Hash:** {tx['tx_hash'] or "N/A"}
        """
    )
