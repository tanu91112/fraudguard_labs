from web3 import Web3

rpc_url = "https://rpc1testnet.qie.digital"
w3 = Web3(Web3.HTTPProvider(rpc_url))

print("Connected:", w3.is_connected())


#python connect_qie_testnet.py
