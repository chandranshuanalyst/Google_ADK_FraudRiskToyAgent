from dotenv import load_dotenv
import os
from google.adk.agents import Agent,ParallelAgent,SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool
from google.genai import types

from tools import (
    get_transaction_data,
    get_behavior_data,
    get_country_data,
    score_transaction_risk,
    score_behavior_risk,
    score_country_risk
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


transaction_researcher = Agent(
    name="TransactionResearcher",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a fraud risk analyst. Your task is to analyze transaction data and provide a risk score.
    Task:
    1. Classify risk as Low / Medium / High
    2. Explain the key drivers
    """,
    tools=[get_transaction_data,score_transaction_risk],
    output_key="transaction_research",
)

print("transaction_researcher created.")

behaviour_researcher = Agent(
    name="BehaviourResearcher",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a fraud risk analyst. Your task is to analyze transaction data and provide a risk score.
    Task:
    1. Classify risk as Low / Medium / High
    2. Explain the key drivers
    """,
    tools=[get_behavior_data,score_behavior_risk],
    output_key="behavior_research",
)

print("behaviour_researcher created.")

country_researcher = Agent(
    name="CountryResearcher",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a fraud risk analyst. Your task is to analyze transaction data and provide a risk score.
    Task:
    1. Classify risk as Low / Medium / High
    2. Explain the key drivers
    """,
    tools=[get_country_data,score_country_risk],
    output_key="country_research",
)

print("country_researcher created.")

aggregator_agent = Agent(
    name="AggregatorAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),

    instruction="""You are a senior fraud analyst. Combine these three research findings into a single executive summary:

    **Transaction Trends:**
    {transaction_research}
    
    **Behavior Trends:**
    {behavior_research}

    **Country Trends:**
    {country_research}


    Tasks:
    1. Provide final risk classification
    2. Recommend action: Approve / Step-up / Block
    3. Summarize key drivers
    4. Suggest next steps

    The final summary should be around 200 words.""",
    output_key="executive_summary",  # This will be the final output of the entire system.
)

print("aggregator_agent created.")

parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[transaction_researcher, behaviour_researcher, country_researcher],
)

# This SequentialAgent defines the high-level workflow: run the parallel team first, then run the aggregator.
root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[parallel_research_team, aggregator_agent],
)

runner = InMemoryRunner(agent=root_agent)
response = runner.run_debug(
    "Run the daily executive fraud risk assessment report for the latest transaction."
)

