from pydantic_ai import Agent
from models.outputs import (
    FinancialSituation, 
    LifeMoment, 
    ChannelPreference, 
    NextBestAction,
    HyperpersonalizedMessage
)
import logfire

logfire.configure()
logfire.instrument_pydantic_ai()

from pydantic_ai.models.google import GoogleModelSettings

# Configure the model settings for Google Gemini 2.5 Flash-Lite
model_settings = GoogleModelSettings(
    google_thinking_config={'thinking_budget': 0}
)

synthesis_agent = Agent(
    'google-gla:gemini-2.5-flash-lite',
    output_type=HyperpersonalizedMessage,
    model_settings=model_settings,
    system_prompt=(
        "You are an expert in customer communication and personalization. "
        "Given insights about a customer's financial situation, life moments, "
        "channel preferences, and recommended actions, craft a highly personalized "
        "message that resonates with their specific context and needs. "
        "The message should be relevant, timely, empathetic, and include a clear call-to-action. "
        "Adapt tone and style based on the customer profile and recommended channel."
    )
)

async def synthesize_message(
    financial: FinancialSituation,
    life_moment: LifeMoment,
    channel: ChannelPreference,
    action: NextBestAction,
    customer_name: str
) -> HyperpersonalizedMessage:
    """Synthesize all insights into personalized message"""
    
    prompt = f"""
Generate a hyperpersonalized message for {customer_name} based on the following insights:

FINANCIAL SITUATION:
- Overall Health: {financial.overall_health}
- Spending Pattern: {financial.spending_pattern}
- Opportunities: {', '.join(financial.opportunities)}

LIFE MOMENTS:
- Detected Moments: {', '.join(life_moment.detected_moments)}
- Time Sensitivity: {life_moment.time_sensitivity}
- Relevant Needs: {', '.join(life_moment.relevant_needs)}

CHANNEL PREFERENCES:
- Primary Channel: {channel.primary_channel}
- Best Contact Time: {channel.best_contact_time}
- Personalization Level: {channel.personalization_level}

RECOMMENDED ACTION:
- Action Type: {action.action_type}
- Recommendation: {action.specific_recommendation}
- Priority: {action.priority}
- Rationale: {action.rationale}

Create a message that:
1. Acknowledges their current situation
2. Addresses their life moment if applicable
3. Presents the recommended action naturally
4. Includes a compelling call-to-action
5. Uses appropriate tone for the {channel.primary_channel} channel
"""
    
    result = await synthesis_agent.run(prompt)
    return result.output
