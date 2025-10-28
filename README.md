# Multi-Agent Financial Analysis System with PydanticAI

A production-ready AI agent system built with PydanticAI and Google Gemini that performs parallel financial analysis to generate hyperpersonalized customer messaging. The system uses deterministic parallel execution across four specialized agents to analyze financial situations, identify life moments, determine communication preferences, and recommend next best actions.

![Solution Architecture](images/solution-diagram.png)

## 🎯 Overview

This system implements a **fan-out, fan-in** architecture pattern where customer data is distributed to multiple specialized agents running in parallel, then converged for synthesis into personalized customer communications.

### Key Features

-   ✅ **Parallel Agent Execution** - Four agents run concurrently using `asyncio.gather()` for optimal performance
-   ✅ **Type-Safe with Pydantic** - All inputs and outputs validated with Pydantic models
-   ✅ **Automatic Retry Logic** - Exponential backoff with jitter for handling API failures
-   ✅ **Structured Outputs** - Strongly-typed agent responses for reliable data flow
-   ✅ **Google Gemini 2.5 Flash-Lite** - Low-latency, cost-efficient LLM for real-time processing
-   ✅ **Dependency Injection** - Clean architecture with shared context across agents
-   ✅ **Production Ready** - Error handling, logging, and resilience patterns built-in

## 🏗️ Architecture

The system consists of five specialized agents:

### Analysis Agents (Parallel Execution)

1. **Financial Analyzer** - Assesses financial health, spending patterns, savings rate, and identifies opportunities
2. **Life Moment Identifier** - Detects significant life events (marriage, new child, home purchase, etc.)
3. **Channel Preference Analyzer** - Determines optimal communication channels and timing
4. **Next Best Action Agent** - Recommends specific products or services

### Synthesis Agent (Sequential)

5. **Message Synthesizer** - Aggregates all insights and generates hyperpersonalized messaging

## 📁 Project Structure

```
financial_agents/
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── main.py                       # Main orchestration and entry point
├── test_gemini.py               # API connectivity test
├── solution-diagram.jpg         # Architecture diagram
├── models/
│   ├── __init__.py
│   ├── customer.py              # Customer profile and transaction models
│   └── outputs.py               # Agent output models (Pydantic)
├── agents/
│   ├── __init__.py
│   ├── financial_analyzer.py   # Financial situation analysis agent
│   ├── life_moment_identifier.py  # Life moment detection agent
│   ├── channel_analyzer.py     # Channel preference agent
│   ├── next_best_action.py     # Next best action recommendation agent
│   └── synthesis_agent.py      # Message synthesis and aggregation agent
├── dependencies/
│   ├── __init__.py
│   └── customer_deps.py        # Dependency injection configuration
└── config/
    ├── __init__.py
    └── retry_config.py         # Retry logic with exponential backoff
```

## 🚀 Getting Started

### Prerequisites

-   Python 3.10 or higher
-   Google API key for Gemini API (get it from [Google AI Studio](https://aistudio.google.com))

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd financial_agents
```

2. **Create and activate virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

Or using `uv` (recommended for faster installation):

```bash
uv pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

### Quick Test

Test your Google Gemini API connection:

```bash
python3 test_gemini.py
```

Expected output:

```
Output: Hello! 👋 How can I help you today?
```

## 🎮 Usage

### Basic Example

Run the system with the sample customer profile:

```bash
python3 main.py
```

### Custom Customer Profile

Modify the `main()` function in `main.py` to use your own customer data:

```python
from datetime import datetime
from models.customer import CustomerProfile, Transaction

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
result = await process_customer_for_personalization(customer)
```

### Example Output

```
Processing customer: CUST_12345
============================================================

🔄 Running parallel analysis agents...
✅ Parallel analysis complete!

📊 Analysis Results:
  Financial Health: good
  Life Moments: New Parent, Medical Expenses
  Best Channel: push_notification
  Recommendation: Open a high-yield savings account for emergency fund

✍️  Generating hyperpersonalized message...
✅ Message generation complete!

============================================================
📧 FINAL PERSONALIZED MESSAGE
============================================================

Channel: push_notification
Subject: Building Your Family's Financial Security

Congratulations on your growing family! We noticed you've been managing
medical expenses recently. Now is the perfect time to strengthen your
financial foundation with a high-yield savings account designed for
families like yours...

Call to Action: Open your account in 3 minutes and start earning 4.5% APY

Optimal Send Time: 7:00 PM
Expected Engagement: 72.5%
```

## 🔧 Configuration

### Model Settings

The system uses Google Gemini 2.5 Flash-Lite by default. To switch models, update the agent definitions:

```python
# In agents/*.py files
financial_analyzer = Agent(
    'google-gla:gemini-2.0-flash',  # Change model here
    deps_type=CustomerDependencies,
    output_type=FinancialSituation,
    model_settings=model_settings,
    system_prompt=...
)
```

Supported models:

-   `google-gla:gemini-2.5-flash-lite` (default, fastest, most cost-efficient)
-   `google-gla:gemini-2.0-flash` (more stable for complex structured outputs)
-   `google-gla:gemini-2.0-flash-thinking` (enhanced reasoning capabilities)
-   `google-gla:gemini-1.5-pro` (highest quality)

### Retry Configuration

Adjust retry behavior in `config/retry_config.py`:

```python
await retry_with_backoff(
    func,
    max_retries=5,           # Maximum retry attempts
    initial_delay=2.0,       # Initial delay in seconds
    max_delay=60.0,          # Maximum delay cap
    exponential_base=2.0     # Exponential backoff multiplier
)
```

### Disable Thinking Mode

Thinking mode is disabled by default to avoid `MALFORMED_FUNCTION_CALL` errors. To enable:

```python
model_settings = GoogleModelSettings(
    google_thinking_config={'thinking_budget': 1024}  # Enable thinking
)
```

## 🏗️ Architecture Patterns

### Parallel Execution

The system uses `asyncio.gather()` for deterministic parallel execution:

```python
tasks = [
    asyncio.create_task(analyze_financial_situation(deps)),
    asyncio.create_task(identify_life_moment(deps)),
    asyncio.create_task(analyze_channel_preference(deps)),
    asyncio.create_task(recommend_next_action(deps))
]

results = await asyncio.gather(*tasks)
```

### Dependency Injection

Shared context is passed to all agents via `CustomerDependencies`:

```python
@dataclass
class CustomerDependencies:
    customer_profile: CustomerProfile
    # Add additional dependencies as needed
```

### Structured Outputs

All agents return validated Pydantic models:

```python
class FinancialSituation(BaseModel):
    overall_health: Literal["excellent", "good", "fair", "poor"]
    spending_pattern: str
    savings_rate: float
    risk_indicators: List[str]
    opportunities: List[str]
```

## 🔍 Troubleshooting

### Common Issues

**1. MALFORMED_FUNCTION_CALL Error**

This occurs when thinking mode conflicts with structured outputs. Solution: Ensure thinking is disabled in model settings.

**2. 503 Service Unavailable**

Google's API is temporarily overloaded. The system automatically retries with exponential backoff. Wait for the retries to complete.

**3. AttributeError: 'AgentRunResult' object has no attribute 'data'**

Use `result.output` instead of `result.data` in PydanticAI v0.6.0+.

**4. Unknown keyword arguments: `result_type`**

Use `output_type` instead of `result_type` in Agent initialization.

### Debug Mode

Enable verbose logging by adding to `main.py`:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance Considerations

-   **Parallel Execution**: 4 agents run concurrently, reducing total execution time by ~75%
-   **Gemini 2.5 Flash-Lite**: Sub-second response times for most requests
-   **Retry Logic**: Automatic handling of transient failures without manual intervention
-   **Token Efficiency**: 1M token context window supports extensive customer history

### Expected Execution Times

-   Single agent: ~1-2 seconds
-   Parallel execution (4 agents): ~2-3 seconds
-   Full pipeline (including synthesis): ~4-6 seconds

## 🧪 Testing

Run the test suite:

```bash
# Test API connectivity
python3 test_gemini.py

# Test full pipeline with sample data
python3 main.py
```

## 🛣️ Roadmap

-   [ ] Add database integration for customer data persistence
-   [ ] Implement caching layer for repeat customer analysis
-   [ ] Add A/B testing framework for message variants
-   [ ] Build REST API wrapper for production deployment
-   [ ] Support batch processing for multiple customers
-   [ ] Implement message delivery tracking
-   [ ] Add customer feedback loop for model improvement

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

-   Built with [PydanticAI](https://ai.pydantic.dev/) by Pydantic
-   Powered by [Google Gemini 2.5 Flash-Lite](https://deepmind.google/models/gemini/flash-lite/)
-   Inspired by multi-agent orchestration patterns from AI agent frameworks

## 📧 Support

For issues, questions, or contributions:

-   Open an issue on GitHub
-   Check the [PydanticAI documentation](https://ai.pydantic.dev/)
-   Review [Google Gemini API documentation](https://ai.google.dev/gemini-api/docs)

---

**Built with ❤️ using PydanticAI and Google Gemini**
