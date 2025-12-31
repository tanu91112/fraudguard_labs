# FraudGuard Architecture

## System Overview

FraudGuard implements a hybrid AI-blockchain architecture where artificial intelligence makes fraud detection decisions and blockchain enforces those decisions with immutable proof.

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Transaction   │───▶│   AI Inference   │───▶│ Smart Contract   │
│   Data          │    │   Engine         │    │   (QIE)          │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                │                        │
                                ▼                        ▼
                      ┌──────────────────┐    ┌──────────────────┐
                      │ Risk Score (0-100)│    │ Automatic Action │
                      └──────────────────┘    └──────────────────┘
```

## Architecture Components

### 1. Off-Chain AI Layer

**Fraud Detection Engine**
- Analyzes transaction patterns in real-time
- Calculates risk scores (0-100) using rule-based and heuristic-driven inference logic
- Identifies fraudulent behavior based on multiple factors

**Input Processing**
- Transaction amount analysis
- Frequency and timing pattern detection
- Address reputation checking
- Network risk assessment

### 2. Blockchain Enforcement Layer

**FraudLog Smart Contract**
- Receives risk scores from AI engine
- Enforces wallet freezing based on the riskScore submitted by the AI engine
- Maintains immutable audit trail of all actions

**Key Functions**
- `logFraud(transactionId, riskScore, walletAddress)` - Records fraud attempt
- `isWalletFrozen(walletAddress)` - Checks wallet status
- `unfreezeWallet(walletAddress)` - Unfreezes wallet (admin only)

### 3. Event System

**Immutable Records**
- `FraudLogged` - Records fraud detection event
- `WalletFrozen` - Records automatic wallet freeze
- `WalletUnfrozen` - Records admin unfreeze action

## Data Flow

1. **Transaction Received**: Transaction data enters the system
2. **AI Analysis**: AI engine calculates risk score based on multiple factors
3. **Risk Assessment**: Risk score compared against configurable off-chain threshold (default: 80)
4. **Blockchain Action**: Smart contract freezes wallet when invoked with a high riskScore by the AI layer
5. **Event Logging**: All actions recorded as blockchain events
6. **Status Verification**: Wallet status can be checked on-chain

## Security Model

**AI Decision Isolation**: AI operates off-chain to protect sensitive data
**Blockchain Enforcement**: Smart contract ensures transparent, tamper-proof execution
**Access Control**: Admin functions protected by owner modifier
**Demo Mode**: Implemented off-chain in the Streamlit interface for hackathon testing

## Technology Stack

**AI Layer**: Python-based inference engine
**Blockchain**: Solidity smart contracts on QIE Testnet
**Interface**: Streamlit application for demonstration
**Events**: Immutable blockchain records for audit trail