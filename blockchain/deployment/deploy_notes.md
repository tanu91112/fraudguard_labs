# FraudLog Contract Deployment Notes

## Contract Information
- **Contract Name**: FraudLog
- **Network**: QIE Testnet
- **Compiler Version**: Solidity ^0.8.0
- **Deployment Date**: December 2025

## Deployment Configuration
- **Owner**: Contract deployer address
- **Risk Threshold**: Controlled off-chain via AI/UI (default: 80)

- **Demo Mode**: Implemented off-chain in Streamlit UI

## Key Addresses & Transactions
- **Contract Address**: 0xD13DAcAe16e579E7bEA9e30E778AcdE61EE1f4b2
- **Deployment Transaction**: 0x59474cd02d1be6be8b54c404587d8945fb456369f396546b4af94d8d9dcdf8e9
- **Verification Status**: Verified on QIE Testnet

## Function Access
- **Public Functions**: `logFraud`, `isWalletFrozen`, `getTransactionCount`, `getTransaction`
- **Owner Only**: `unfreezeWallet`

## Testing Instructions
1. Ensure demoMode is enabled for hackathon testing
2. Call `logFraud` with riskScore ≥ 80 to test automatic wallet freezing
3. Verify wallet status with `isWalletFrozen`
4. Use `unfreezeWallet` to reset for next test
5. Check emitted events for audit trail verification

## Security Notes
- Risk threshold is configurable by owner
- Wallet freezing occurs within `logFraud()` when the submitted riskScore meets freeze conditions
- Only owner can unfreeze wallets
- Demo mode allows testing without owner privileges

