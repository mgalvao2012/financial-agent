from pydantic_ai import Agent, RunContext
from models.outputs import NextBestAction
from dependencies.customer_deps import CustomerDependencies
from pydantic_ai.models.google import GoogleModelSettings
import logfire

logfire.configure()
logfire.instrument_pydantic_ai()

# Configure the model settings for Google Gemini 2.5 Flash-Lite
model_settings = GoogleModelSettings(
    google_thinking_config={'thinking_budget': 0}
)

nba_agent = Agent(
    'google-gla:gemini-2.5-flash-lite',
    deps_type=CustomerDependencies,
    output_type=NextBestAction, 
    model_settings=model_settings,
    system_prompt=(
        "You are a banking product specialist and relationship manager. "
        "Based on customer financial situation and needs, recommend the most "
        "appropriate next best action or offer. Consider products like: "
        "savings accounts, credit cards, loans, investment products, "
        "insurance, or financial advisory services. "
        "Prioritize recommendations that provide genuine customer value."
    )
)

@nba_agent.system_prompt
def add_product_context(ctx: RunContext[CustomerDependencies]) -> str:
    """Add context for product recommendations"""
    profile = ctx.deps.customer_profile
    
    return f"""
Customer Financial Profile:
- Income: ${profile.income:,.2f}
- Account Balance: ${profile.account_balance:,.2f}
- Credit Score: {profile.credit_score or 'Not available'}
- Age: {profile.age}
"""

async def recommend_next_action(deps: CustomerDependencies) -> NextBestAction:
    """Generate next best action recommendation"""
    result = await nba_agent.run(
        "Recommend the next best action or offer for this customer.",
        deps=deps
    )
    return result.output  # Changed from result.data to result.output
