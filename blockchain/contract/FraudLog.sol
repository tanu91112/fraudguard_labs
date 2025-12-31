// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FraudLog {
    // Events
    event FraudLogged(
        bytes32 transactionId,
        uint256 riskScore,
        address walletAddress,
        uint256 timestamp
    );

    event WalletFrozen(
        address walletAddress,
        bytes32 transactionId,
        uint256 riskScore,
        uint256 timestamp
    );

    event WalletUnfrozen(
        address walletAddress,
        address admin,
        uint256 timestamp
    );

    // State
    mapping(bytes32 => bool) public flaggedTransactions;
    mapping(address => bool) public frozenWallets;
    mapping(bytes32 => address) public transactionWallets;

    uint256 public riskThreshold = 80;
    address public owner;

    // Demo mode for hackathon testing
    bool public demoMode = true;

    struct Transaction {
        bytes32 id;
        uint256 risk;
        address wallet;
        uint256 timestamp;
    }

    Transaction[] public transactions;

    // Only owner modifier
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    // Owner or demo mode modifier
    modifier onlyOwnerOrDemo() {
        require(demoMode || msg.sender == owner, "Only owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    // Log a fraud attempt and freeze wallet if riskScore >= riskThreshold
    function logFraud(
        bytes32 transactionId,
        uint256 riskScore,
        address walletAddress
    ) public onlyOwnerOrDemo {
        require(transactionId != bytes32(0), "Transaction ID required");
        require(walletAddress != address(0), "Invalid wallet address");
        require(riskScore <= 100, "Risk score must be 0-100");

        flaggedTransactions[transactionId] = true;
        transactionWallets[transactionId] = walletAddress;

        // Save transaction to history (optional if hitting gas limits)
        transactions.push(Transaction(transactionId, riskScore, walletAddress, block.timestamp));

        emit FraudLogged(transactionId, riskScore, walletAddress, block.timestamp);

        if (riskScore >= riskThreshold) {
            frozenWallets[walletAddress] = true;
            emit WalletFrozen(walletAddress, transactionId, riskScore, block.timestamp);
        }
    }

    // Unfreeze a wallet (only owner)
    function unfreezeWallet(address walletAddress) public onlyOwner {
        require(walletAddress != address(0), "Invalid wallet address");
        frozenWallets[walletAddress] = false;
        emit WalletUnfrozen(walletAddress, msg.sender, block.timestamp);
    }

    // Set new risk threshold (only owner)
    function setRiskThreshold(uint256 newThreshold) public onlyOwner {
        require(newThreshold > 0 && newThreshold <= 100, "Threshold 1-100");
        riskThreshold = newThreshold;
    }

    // Check if wallet is frozen
    function isWalletFrozen(address walletAddress) public view returns (bool) {
        require(walletAddress != address(0), "Invalid wallet address");
        return frozenWallets[walletAddress];
    }

    // Check if transaction is flagged
    function isTransactionFlagged(bytes32 transactionId) public view returns (bool) {
        require(transactionId != bytes32(0), "Transaction ID required");
        return flaggedTransactions[transactionId];
    }

    // Get total number of transactions logged
    function getTransactionCount() public view returns (uint256) {
        return transactions.length;
    }

    // Optional: get transaction by index
    function getTransaction(uint256 index) public view returns (bytes32, uint256, address, uint256) {
        require(index < transactions.length, "Index out of bounds");
        Transaction memory t = transactions[index];
        return (t.id, t.risk, t.wallet, t.timestamp);
    }

    // Toggle demo mode (only owner)
    function setDemoMode(bool mode) public onlyOwner {
        demoMode = mode;
    }
}
