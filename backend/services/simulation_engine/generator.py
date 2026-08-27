"""
High-Volume Financial Transaction Simulator
"""

import random
import uuid
from backend.core.types import TransactionEvent


class FinancialTrafficGenerator:
    def __init__(self, num_users: int = 500):
        self.users = [f"usr_{i:04d}" for i in range(num_users)]
        self.merchants = [f"merch_{i:03d}" for i in range(50)]

    def generate_single_transaction(self, is_fraud: bool = False) -> TransactionEvent:
        user_id = random.choice(self.users)
        amount = round(random.uniform(500.0, 4500.0) if is_fraud else random.uniform(5.0, 150.0), 2)

        return TransactionEvent(
            transaction_id=f"tx_{str(uuid.uuid4())[:12]}",
            user_id=user_id,
            source_account_id=f"acct_{user_id}",
            target_account_id=f"acct_{random.choice(self.merchants)}",
            amount=amount,
            currency="USD",
            merchant_id=random.choice(self.merchants),
            device_id=f"dev_{user_id}" if not is_fraud else f"dev_fraud_{random.randint(1, 10)}",
            ip_address=f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
            latitude=round(random.uniform(25.0, 48.0), 4),
            longitude=round(random.uniform(-120.0, -70.0), 4),
            channel="mobile_app",
        )


traffic_generator = FinancialTrafficGenerator()
