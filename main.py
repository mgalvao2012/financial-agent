import asyncio
import logfire
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv

logfire.configure()  
logfire.instrument_pydantic_ai()

# Load environment variables
load_dotenv()

from models.customer import CustomerProfile, Transaction
from dependencies.customer_deps import CustomerDependencies
from agents.financial_analyzer import analyze_financial_situation
from agents.life_moment_identifier import identify_life_moment
from agents.channel_analyzer import analyze_channel_preference
from agents.next_best_action import recommend_next_action
from agents.synthesis_agent import synthesize_message

async def process_customer_for_personalization(customer_profile: CustomerProfile) -> dict:
    """
    Main orchestration function that runs all agents in parallel
    and synthesizes the results into a hyperpersonalized message.
    """
    
    print(f"Processing customer: {customer_profile.customer_id}")
    print("=" * 60)
    
    # Create dependencies
    deps = CustomerDependencies(customer_profile=customer_profile)
    
    # Step 1: Run parallel agent execution for data gathering
    print("\n🔄 Running parallel analysis agents...")
    
    # Create tasks for concurrent execution
    tasks = [
        asyncio.create_task(analyze_financial_situation(deps)),
        asyncio.create_task(identify_life_moment(deps)),
        asyncio.create_task(analyze_channel_preference(deps)),
        asyncio.create_task(recommend_next_action(deps))
    ]
    
    # Execute all agents in parallel using asyncio.gather
    results = await asyncio.gather(*tasks)
    
    # Unpack results
    financial_situation, life_moment, channel_preference, next_best_action = results
    
    print("✅ Parallel analysis complete!")
    
    # Display intermediate results
    print("\n📊 Analysis Results:")
    print(f"  Financial Health: {financial_situation.overall_health}")
    print(f"  Life Moments: {', '.join(life_moment.detected_moments) or 'None detected'}")
    print(f"  Best Channel: {channel_preference.primary_channel}")
    print(f"  Recommendation: {next_best_action.specific_recommendation}")
    
    # Step 2: Synthesize insights into personalized message
    print("\n✍️  Generating hyperpersonalized message...")
    
    personalized_message = await synthesize_message(
        financial=financial_situation,
        life_moment=life_moment,
        channel=channel_preference,
        action=next_best_action,
        customer_name=f"Customer {customer_profile.customer_name}"
    )
    
    print("✅ Message generation complete!")
    
    # Return comprehensive results
    return {
        "customer_id": customer_profile.customer_id,
        "analysis": {
            "financial_situation": financial_situation.model_dump(),
            "life_moment": life_moment.model_dump(),
            "channel_preference": channel_preference.model_dump(),
            "next_best_action": next_best_action.model_dump()
        },
        "personalized_message": personalized_message.model_dump()
    }

async def main():
    """Main entry point with sample customer data"""
    
    # Sample customer profile
    customer = CustomerProfile(
        customer_id="CUST_12345",
        customer_name="Jane Doe",
        age=32,
        income=85000.0,
        account_balance=15000.0,
        credit_score=720,
        recent_transactions=[
            Transaction(
                amount=1200.0,
                category="rent",
                date=datetime.now() - timedelta(days=5),
                merchant="Property Management"
            ),
            Transaction(
                amount=450.0,
                category="baby_supplies",
                date=datetime.now() - timedelta(days=10),
                merchant="Baby Store"
            ),
            Transaction(
                amount=2800.0,
                category="medical",
                date=datetime.now() - timedelta(days=15),
                merchant="Hospital"
            )
        ],
        location="San Francisco, CA",
        marital_status="married",
        employment_status="employed",
        has_children=True,
        preferred_contact_times=["evening", "weekend"],
        digital_engagement={
            "mobile_app_sessions_per_week": 12,
            "email_open_rate": 0.65,
            "push_notification_enabled": True
        },
        account_data={
            "debts": [1200, 800]  # monthly obligations
        }
    )
    
    # Process customer
    result = await process_customer_for_personalization(customer)
    
    # Display final message
    print("\n" + "=" * 60)
    print("📧 FINAL PERSONALIZED MESSAGE")
    print("=" * 60)
    print(f"\nChannel: {result['personalized_message']['recommended_channel']}")
    print(f"Subject: {result['personalized_message']['message_subject']}")
    print(f"\n{result['personalized_message']['message_body']}")
    print(f"\nCall to Action: {result['personalized_message']['call_to_action']}")
    print(f"\nOptimal Send Time: {result['personalized_message']['optimal_send_time']}")
    print(f"Expected Engagement: {result['personalized_message']['expected_engagement_rate']:.1%}")
    
    return result

if __name__ == "__main__":
    start_time = datetime.now()
    # Run the async main function
    result = asyncio.run(main())
    end_time = datetime.now()
    dif_time = end_time - start_time
    print('='*60)
    print(f"\"{start_time}\",\"{end_time}\",\"{dif_time}\"")
    print('='*60)