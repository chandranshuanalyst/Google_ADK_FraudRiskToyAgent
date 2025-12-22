from dotenv import load_dotenv
import os
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search,AgentTool
from google.genai import types



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


gst_agent = Agent(
    name="gst_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="You are a gst assistant. Your task is to help users with gst related queries.",
    instruction="""
    You are a gst assistant. Your task is to help users with gst related queries.
    Your queries may include topics such as gst registration, filing returns, compliance requirements, and tax rates.
    Use the google search tool to find relevant and up-to-date information on gst topics.
    Provide concise and accurate answers based on your findings.
    """,
    tools=[google_search],
    output_key="gst_assistant_response",
)

writer_agent = Agent(
    name="writer_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="You are writer assistant who is expert at summarizing information concisely and accurately. You get the research information from researchers and you write it in a clear and concise manner.",
    instruction="""
    You are a writer assistant who is expert at summarizing information concisely and accurately.
    You will receive research information from researchers.
    Your task is to:
    1. Summarize the key findings from the research information.
    2. Write it in a clear and concise manner.
    3. Ensure the summary is easy to understand for a general audience.
    4. Keep the summary within 200 words.
    """,
    output_key="writer_assistant_response",
)

sales_agent = Agent(
    name="sales_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="You are sales assistant who is expert at generating sales emails based on research information provided by researchers.",
    instruction="""
    You are a sales assistant who is expert at generating sales emails.
    You will receive research information from researchers.
    Your task is to:
    1. Generate a persuasive sales email based on the research information.
    2. Highlight the key benefits and features of the product or service.
    3. Use a professional and engaging tone.
    4. Keep the email within 150 words.
    """,
    output_key="sales_assistant_response",
)

root_agent = Agent(
    name="RootAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="You are the root agent coordinating between gst assistant, writer assistant, and sales assistant to provide comprehensive responses.",
    instruction="""
    You are the root agent coordinating between gst assistant, writer assistant, and sales assistant.
    Your task is to:
    1. Direct gst-related queries to the gst assistant.
    2. Forward research information to the writer assistant for summarization.
    3. Send relevant information to the sales assistant for email generation.
    4. Compile and present the final responses from all assistants in a coherent manner.
    """,
    tools=[AgentTool(gst_agent), AgentTool(writer_agent), AgentTool(sales_agent)],
)



print("Root Agent defined.")


runner = InMemoryRunner(agent=root_agent)

print("Runner created.")

runner.run_debug("A client needs assistance with GST registration and wants a sales email to promote our GST consultancy services."
)

