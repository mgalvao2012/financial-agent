from pydantic_ai import Agent, RunContext
from models.outputs import LifeMoment
from dependencies.customer_deps import CustomerDependencies
from pydantic_ai.models.google import GoogleModelSettings
import logfire

logfire.configure()
logfire.instrument_pydantic_ai()

# Configure the model settings for Google Gemini 2.5 Flash-Lite
model_settings = GoogleModelSettings(
    google_thinking_config={'thinking_budget': 0}
)

life_moment_agent = Agent(
    'google-gla:gemini-2.5-flash-lite',
    deps_type=CustomerDependencies,
    output_type=LifeMoment,  # Changed from result_type to output_type
    model_settings=model_settings,
    system_prompt=(
        "You are an expert in customer lifecycle analysis. "
        "Identify significant life moments and transitions based on financial behavior, "
        "demographic information, and transaction patterns. "
        "Life moments include: career changes, relocation, marriage, new child, "
        "home purchase, retirement planning, education expenses, etc. "
        "Assess confidence and time sensitivity for each detected moment."
    )
)

@life_moment_agent.system_prompt
def add_life_context(ctx: RunContext[CustomerDependencies]) -> str:
    """Add customer life context"""
    profile = ctx.deps.customer_profile
    transaction_categories = [t.category for t in profile.recent_transactions]
    
    return f"""
Customer Life Context:
- Age: {profile.age}
- Marital Status: {profile.marital_status or 'Unknown'}
- Has Children: {profile.has_children}
- Employment: {profile.employment_status or 'Unknown'}
- Location: {profile.location}
- Transaction Categories: {', '.join(set(transaction_categories))}
"""

async def identify_life_moment(deps: CustomerDependencies) -> LifeMoment:
    """Identify customer life moments"""
    result = await life_moment_agent.run(
        "Identify any significant life moments or transitions for this customer.",
        deps=deps
    )
    return result.output  # Changed from result.data to result.output
