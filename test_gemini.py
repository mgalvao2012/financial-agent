from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

agent = Agent('google-gla:gemini-2.5-flash-lite')

async def test():
    result = await agent.run("Say hello!")
    
    # Access the output
    print("Output:", result.output)
    
    # Optional: See all available attributes
    print("\nResult attributes:", dir(result))
    
    # Optional: See the full result object
    print("\nFull result:", result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())