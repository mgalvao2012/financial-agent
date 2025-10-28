from dataclasses import dataclass
from models.customer import CustomerProfile

@dataclass
class CustomerDependencies:
    """Dependencies passed to all agents"""
    customer_profile: CustomerProfile
    # Add additional dependencies as needed
    # db_connection: Optional[Any] = None
    # api_client: Optional[Any] = None
