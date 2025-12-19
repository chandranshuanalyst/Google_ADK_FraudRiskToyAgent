from dotenv import load_dotenv
import os
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

from tools import (
    fetch_transaction_data,
    fetch_customer_snapshot,
    fraud_model_proxy
)

print("ADK components imported successfully.")


load_dotenv()

try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    print("Gemini API key setup complete.")
except Exception as e:
    print(
        f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' to your Kaggle secrets. Details: {e}"
    )
    
retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)



root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="You are a fraud risk analyst at a bank. You have access to the live customer data and transaction data. Use the tools to fetch data. Then you have a fraud model that gives you some important metrics like fraud score, amount ratio, velocity etc. Based on these metrics, use your decision engine to classify risk level and recommend action.",
    instruction="""
    As a 1st step take the transaction data from fetch_transaction_data tool.
    As a 2nd step take the customer snapshot from fetch_customer_snapshot tool.
    Then pass the data to the fraud_model_proxy tool to get the risk signals.
    Finally, use the llm_decision_engine to:    
    - Classify risk as Low / Medium / High
    - Recommend action: Approve / Step-up Authentication / Block
    - Provide a short explanation referencing the signals
    
    An exmple response format is:
    Risk Level: Low
    Action: Approve

    Explanation:
    Low fraud score driven by normal transaction amount, velocity, international merchant, and CNP channel.
    
    Keep your answers concise and to the point. and stick to the format of output as given in example. Donot copy the example response. 
    """,
    tools=[fetch_transaction_data,fetch_customer_snapshot,fraud_model_proxy],
)

print("Root Agent defined.")


runner = InMemoryRunner(agent=root_agent)

print("Runner created.")

runner.run_debug("Run scheduled fraud risk assessment for the latest transaction and return decision"
)

