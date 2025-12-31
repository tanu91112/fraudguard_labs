# FraudGuard AI Model Information

## Model Type
The FraudGuard AI system implements a **rule-based risk scoring engine** that simulates real AI/ML fraud detection. In a production environment, this would be replaced with a trained machine learning model, but for hackathon demonstration purposes, we use weighted rule-based logic.

## Input Features (Conceptual)

The AI model analyzes the following transaction features:

**Transaction Amount**
- Risk increases with higher transaction values
- Threshold-based risk assignment

**Transaction Frequency**
- Number of recent transactions from same wallet
- Time-based transaction clustering

**Time Anomalies**
- Transactions at unusual hours
- Timing patterns that suggest fraudulent behavior

**Address Reputation**
- Wallet address history and reputation
- Known fraud address matching

**Network Risk**
- Connected address analysis
- Transaction graph patterns

## Output Logic

**Risk Score (0-100)**
- 0-20: Very Low Risk
- 21-40: Low Risk  
- 41-60: Medium Risk
- 61-79: High Risk
- 80-100: Very High Risk (Triggers wallet freeze)

**Decision Threshold**
- Risk score ≥ 80: Automatically freeze wallet
- Risk score < 80: Log transaction, no action

## Why Dataset is Abstracted

**Real-World Privacy**: Financial transaction data contains sensitive personal information that cannot be shared or used in public demonstrations.

**Security**: Actual fraud patterns and detection methods are proprietary and must be protected.

**Regulatory Compliance**: Financial data is subject to strict privacy regulations (GDPR, CCPA, etc.).

**Scalability**: The model demonstrates the concept without requiring access to large datasets, showing how the system would work with real data.

## Model Architecture

The system uses a weighted combination of risk factors:

- Amount Anomaly: 30%
- Frequency Anomaly: 25%
- Time Anomaly: 20%
- Address Reputation: 15%
- Network Risk: 10%

## Integration with Blockchain

The AI model operates off-chain for computational efficiency and privacy. Risk scores are transmitted to the QIE Blockchain smart contract which automatically enforces wallet freezing decisions based on the risk threshold.# FraudGuard AI Model Information

## Model Type
The FraudGuard system uses an **AI-inspired heuristic risk scoring engine** for real-time fraud detection.  
For this hackathon prototype, the system performs **inference-only risk evaluation** using weighted anomaly indicators.  
In a production environment, this logic can be replaced with a fully trained machine learning model.

## Input Features (Conceptual)

The system evaluates transactions using the following fraud-related indicators:

**Transaction Amount**
- Higher transaction values increase risk
- Threshold-based anomaly scoring

**Transaction Frequency**
- Rapid or clustered transactions from the same wallet
- Short time gaps between consecutive transactions

**Time Anomalies**
- Transactions occurring at unusual or suspicious time windows

**Address Reputation**
- Known suspicious or previously flagged wallet patterns
- Historical risk indicators

**Network Risk**
- Simple connected-address risk signals
- Transaction relationship indicators

## Output Logic

**Risk Score (0–100)**
- 0–20: Very Low Risk
- 21–40: Low Risk  
- 41–60: Medium Risk
- 61–79: High Risk
- 80–100: Very High Risk

**Decision Threshold**
- Risk score ≥ 80: Wallet is flagged and eligible for smart-contract action
- Risk score < 80: Transaction is logged with no enforcement action

## Why Dataset is Abstracted

**Privacy**: Financial transaction data contains sensitive user information that cannot be exposed in public demonstrations.

**Security**: Real-world fraud detection rules and patterns are proprietary and must be protected.

**Regulatory Compliance**: Financial data is governed by strict regulations such as GDPR and CCPA.

**Demonstration Focus**: The prototype demonstrates the complete AI-to-blockchain workflow without requiring access to real datasets.

## Model Architecture

The overall risk score is computed using a weighted combination of anomaly indicators:

- Amount Anomaly: 30%
- Frequency Anomaly: 25%
- Time Anomaly: 20%
- Address Reputation: 15%
- Network Risk: 10%

This structure reflects how real-world fraud detection systems combine multiple risk signals.

## Integration with Blockchain

The risk scoring logic runs **off-chain** for computational efficiency and privacy.  
Final risk scores and fraud flags are transmitted to the **QIE Blockchain smart contract**, which:

- Logs fraud-related events immutably on-chain
- Applies rule-based contract actions (flag / freeze simulation)
- Emits audit events for real-time dashboard visualization
