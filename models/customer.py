from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Transaction(BaseModel):
    """Individual transaction record"""
    amount: float
    category: str
    date: datetime
    merchant: Optional[str] = None

class CustomerProfile(BaseModel):
    """Customer profile with all available data"""
    customer_id: str
    customer_name: str
    age: int
    income: float
    account_balance: float
    credit_score: Optional[int] = None
    recent_transactions: List[Transaction] = []
    location: str
    marital_status: Optional[str] = None
    employment_status: Optional[str] = None
    has_children: bool = False
    preferred_contact_times: List[str] = []
    digital_engagement: dict = {}  # app usage, email opens, etc.
    account_data: dict = {}  # income, debts, credit score, etc.
