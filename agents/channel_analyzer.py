from pydantic_ai import Agent, RunContext
from models.outputs import ChannelPreference
from dependencies.customer_deps import CustomerDependencies
from pydantic_ai.models.google import GoogleModelSettings
import logfire

logfire.configure()
logfire.instrument_pydantic_ai()

# Configure the model settings for Google Gemini 2.5 Flash-Lite
model_settings = GoogleModelSettings(
    google_thinking_config={'thinking_budget': 0}
)

channel_agent = Agent(
    'google-gla:gemini-2.5-flash-lite',
    deps_type=CustomerDependencies,
    output_type=ChannelPreference,  # Changed from result_type to output_type
    model_settings=model_settings,
    system_prompt=(
        "You are a customer engagement specialist. "
        "Analyze customer digital behavior and preferences to determine "
        "the most effective communication channels and optimal contact times. "
        "Consider engagement history, demographic factors, and behavioral patterns."
    )
)

@channel_agent.system_prompt
def add_engagement_context(ctx: RunContext[CustomerDependencies]) -> str:
    """Add engagement context"""
    profile = ctx.deps.customer_profile
    
    return f"""
Customer Engagement Profile:
- Age: {profile.age}
- Location: {profile.location}
- Preferred Contact Times: {', '.join(profile.preferred_contact_times) or 'Not specified'}
- Digital Engagement: {profile.digital_engagement}
"""

async def analyze_channel_preference(deps: CustomerDependencies) -> ChannelPreference:
    """Determine best communication channel"""
    result = await channel_agent.run(
        "Determine the best communication channels and timing for this customer.",
        deps=deps
    )
    return result.output  # Changed from result.data to result.output
