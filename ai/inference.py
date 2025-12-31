"""
FraudGuard AI Inference Engine
Off-chain AI model for fraud detection and risk scoring
"""

import hashlib
import time
import random
from typing import Dict, Any


class FraudDetectionAI:
    """
    Simple rule-based AI model for fraud detection.
    In a real implementation, this would use ML models,
    but for hackathon purposes we use rule-based logic.
    """
    
    def __init__(self):
        # Risk factors weights (for demonstration purposes)
        self.risk_factors = {
            'amount_anomaly': 0.3,
            'frequency_anomaly': 0.25,
            'time_anomaly': 0.2,
            'address_reputation': 0.15,
            'network_risk': 0.1
        }
    
    def calculate_risk_score(self, transaction_data: Dict[str, Any]) -> int:
        """
        Calculate risk score (0-100) based on transaction data
        
        Args:
            transaction_data: Dictionary containing transaction details
            
        Returns:
            Risk score as integer between 0-100
        """
        # Extract transaction features
        amount = transaction_data.get('amount', 0)
        wallet_address = transaction_data.get('wallet_address', '')
        timestamp = transaction_data.get('timestamp', int(time.time()))
        recent_transactions = transaction_data.get('recent_transactions', [])
        
        # Calculate individual risk factors
        amount_risk = self._calculate_amount_risk(amount)
        frequency_risk = self._calculate_frequency_risk(recent_transactions)
        time_risk = self._calculate_time_risk(timestamp)
        address_risk = self._calculate_address_risk(wallet_address)
        network_risk = self._calculate_network_risk(wallet_address)
        
        # Weighted risk calculation
        total_risk = (
            amount_risk * self.risk_factors['amount_anomaly'] +
            frequency_risk * self.risk_factors['frequency_anomaly'] +
            time_risk * self.risk_factors['time_anomaly'] +
            address_risk * self.risk_factors['address_reputation'] +
            network_risk * self.risk_factors['network_risk']
        )
        
        # Convert to 0-100 scale
        risk_score = min(100, max(0, int(total_risk * 100)))
        
        return risk_score
    
    def _calculate_amount_risk(self, amount: float) -> float:
        """Calculate risk based on transaction amount"""
        # Higher amounts have higher risk (capped)
        if amount > 10000:  # Very high amount
            return 0.9
        elif amount > 5000:  # High amount
            return 0.7
        elif amount > 1000:  # Medium amount
            return 0.4
        else:  # Low amount
            return 0.1
    
    def _calculate_frequency_risk(self, recent_transactions: list) -> float:
        """Calculate risk based on transaction frequency"""
        if len(recent_transactions) > 10:  # Very frequent
            return 0.9
        elif len(recent_transactions) > 5:  # Frequent
            return 0.7
        elif len(recent_transactions) > 2:  # Moderate
            return 0.4
        else:  # Normal
            return 0.1
    
    def _calculate_time_risk(self, timestamp: int) -> float:
        """Calculate risk based on transaction time"""
        # Check if transaction happens at unusual hours
        current_hour = (timestamp % 86400) // 3600  # Hour of day (0-23)
        
        # High risk if transaction occurs during unusual hours (2 AM - 5 AM)
        if 2 <= current_hour <= 5:
            return 0.7
        else:
            return 0.2
    
    def _calculate_address_risk(self, address: str) -> float:
        """Calculate risk based on wallet address reputation"""
        # Simulate address reputation check
        # In real system, this would check against known fraud addresses
        address_hash = hashlib.sha256(address.encode()).hexdigest()
        
        # Simulate some addresses being high risk
        if address_hash.startswith(('00', 'ff', 'aa')):
            return 0.8
        elif address_hash.startswith(('0', '1', '2')):
            return 0.5
        else:
            return 0.2
    
    def _calculate_network_risk(self, address: str) -> float:
        """Calculate risk based on network analysis"""
        # Simulate network risk (connected addresses, etc.)
        address_hash = hashlib.sha256(address.encode()).hexdigest()
        
        # Random risk factor based on address properties
        if len(set(address_hash)) < 10:  # Less entropy = suspicious
            return 0.6
        else:
            return 0.3
    
    def predict_fraud(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main prediction function that returns fraud prediction results
        
        Args:
            transaction_data: Transaction details
            
        Returns:
            Dictionary with prediction results
        """
        risk_score = self.calculate_risk_score(transaction_data)
        
        # Generate transaction ID based on transaction data
        transaction_id = hashlib.sha256(
            f"{transaction_data.get('wallet_address', '')}{transaction_data.get('amount', 0)}{transaction_data.get('timestamp', int(time.time()))}".encode()
        ).hexdigest()
        
        result = {
            'transaction_id': transaction_id,
            'risk_score': risk_score,
            'is_fraud': risk_score >= 80,  # Threshold for fraud classification
            'confidence': min(1.0, risk_score / 100.0),  # Confidence based on risk score
            'risk_breakdown': {
                'amount_risk': self._calculate_amount_risk(transaction_data.get('amount', 0)),
                'frequency_risk': self._calculate_frequency_risk(transaction_data.get('recent_transactions', [])),
                'time_risk': self._calculate_time_risk(transaction_data.get('timestamp', int(time.time()))),
                'address_risk': self._calculate_address_risk(transaction_data.get('wallet_address', '')),
                'network_risk': self._calculate_network_risk(transaction_data.get('wallet_address', ''))
            }
        }
        
        return result


# Mock function to simulate AI inference for demo purposes
def get_mock_risk_score(amount, wallet_address, transaction_count, is_suspicious_time=False):
    """
    Generate mock risk score for demo purposes
    
    Args:
        amount: Transaction amount
        wallet_address: Wallet address involved
        transaction_count: Number of recent transactions
        is_suspicious_time: Whether transaction is at suspicious time
    
    Returns:
        Risk score between 0-100
    """
    base_risk = 0
    
    # Amount-based risk
    if amount > 10000:
        base_risk += 40
    elif amount > 5000:
        base_risk += 30
    elif amount > 1000:
        base_risk += 15
    else:
        base_risk += 5
    
    # Frequency-based risk
    if transaction_count > 10:
        base_risk += 35
    elif transaction_count > 5:
        base_risk += 25
    elif transaction_count > 2:
        base_risk += 15
    else:
        base_risk += 5
    
    # Time-based risk
    if is_suspicious_time:
        base_risk += 20
    
    # Address-based risk (simulated)
    if wallet_address and len(wallet_address) > 0:
        address_factor = sum(ord(c) for c in wallet_address[:5]) % 30
        base_risk += address_factor
    
    # Add some randomness for realism
    risk_score = min(100, max(0, base_risk + random.randint(-10, 15)))
    
    return risk_score


# Example usage
if __name__ == "__main__":
    # Example transaction data
    sample_transaction = {
        'amount': 7500,
        'wallet_address': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'timestamp': int(time.time()),
        'recent_transactions': [1, 2, 3, 4, 5, 6]  # 6 recent transactions
    }
    
    # Initialize AI model
    ai_model = FraudDetectionAI()
    
    # Get prediction
    result = ai_model.predict_fraud(sample_transaction)
    
    print("Fraud Detection Results:")
    print(f"Transaction ID: {result['transaction_id'][:16]}...")
    print(f"Risk Score: {result['risk_score']}")
    print(f"Is Fraud: {result['is_fraud']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print("Risk Breakdown:", result['risk_breakdown'])