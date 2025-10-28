from pydantic_ai import Agent, RunContext
from models.outputs import FinancialSituation
from dependencies.customer_deps import CustomerDependencies
from pydantic_ai.models.google import GoogleModelSettings
import logfire

logfire.configure()
logfire.instrument_pydantic_ai()

# Configure the model settings for Google Gemini 2.5 Flash-Lite
model_settings = GoogleModelSettings(
    google_thinking_config={'thinking_budget': 0}
)

# Create the financial analyzer agent with Gemini 2.5 Flash-Lite
financial_analyzer = Agent(
    'google-gla:gemini-2.5-flash-lite',
    deps_type=CustomerDependencies,
    output_type=FinancialSituation,  # Changed from result_type to output_type
    model_settings=model_settings,
    system_prompt=(
        "You are an expert financial analyst specializing in consumer banking. "
        "Analyze customer financial data to assess overall financial health, "
        "identify spending patterns, calculate savings rates, detect risk indicators, "
        "and uncover opportunities for financial improvement. "
        "Provide actionable insights based on transaction history, income, and account balance."
    )
)

@financial_analyzer.tool
async def calculate_debt_ratio(ctx: RunContext[CustomerDependencies]) -> float:
    """Calculate debt-to-income ratio deterministically"""
    profile = ctx.deps.customer_profile
    account_data = profile.account_data
    monthly_debt = sum(account_data.get('debts', []))
    monthly_income = profile.income / 12  # Assuming income is annual
    return monthly_debt / monthly_income if monthly_income > 0 else 0.0

@financial_analyzer.tool
async def get_spending_pattern(ctx: RunContext[CustomerDependencies]) -> str:
    """Analyze spending by category"""
    profile = ctx.deps.customer_profile
    transactions = profile.recent_transactions
    categories = {}
    for txn in transactions:
        category = txn.category
        amount = txn.amount
        categories[category] = categories.get(category, 0) + amount
    return categories

@financial_analyzer.system_prompt
def add_customer_context(ctx: RunContext[CustomerDependencies]) -> str:
    """Add dynamic customer context to system prompt"""
    profile = ctx.deps.customer_profile
    return f"""
Customer Context:
- Customer ID: {profile.customer_id}
- Age: {profile.age}
- Income: ${profile.income:,.2f}
- Account Balance: ${profile.account_balance:,.2f}
- Credit Score: {profile.credit_score or 'Not available'}
- Recent Transactions: {len(profile.recent_transactions)} transactions
"""

async def analyze_financial_situation(deps: CustomerDependencies) -> FinancialSituation:
    """Run the financial analysis"""
    result = await financial_analyzer.run(
        "Analyze this customer's financial situation based on the provided data.",
        deps=deps
    )
    return result.output  # Changed from result.data to result.output