# Google ADK Demo - from a financial use case perspective

This small project contains three example agent setups that show different ways to organize AI helpers (called "agents") for tasks like research, summarization, and risk scoring. The examples use Google ADK components and are intended to be easy to run and explore.

If you are not a developer, think of each example as a small program demonstrating how to give an AI a job and some helper tools, then ask it to do that job.

**What's in this project**
- `my_agent`: A single agent that runs a fraud risk check using helper functions.
- `multi_agent`: Several specialist agents (researcher, writer, sales) coordinated by a root agent.
- `my_parallel_agent`: Runs multiple researchers in parallel and then combines their findings into one executive summary.
- `myenv`: A local Python virtual environment (optional)
- `requirements.txt`: Python dependencies for the project.

**Quick start (Windows)**
1. Activate the virtual environment (if you want to use the included `myenv`):

```powershell
myenv\Scripts\Activate.ps1
```

or (cmd.exe):

```cmd
myenv\Scripts\activate.bat
```

2. Install dependencies (if not already installed):

```bash
pip install -r requirements.txt
```

3. Set the required API key. The agents expect a `GOOGLE_API_KEY` environment variable. You can add it to a `.env` file in the package folder or set it in your environment. Example (Windows cmd):

```cmd
set GOOGLE_API_KEY=your_api_key_here
```

**Run an example**
- Single-agent fraud example:

```bash
python my_agent/agent.py
```

- Multi-agent coordination example:

```bash
python multi_agent/agent.py
```

- Parallel researchers + aggregator example:

```bash
python my_parallel_agent/agent.py
```

What to expect: each script builds a small AI workflow and runs it with an in-memory runner. Output is printed to the console showing the agent's response.

**Plain-language descriptions**
- `my_agent`: One AI that fetches data, runs a fraud check, and returns a short decision (Approve / Step-up / Block).
- `multi_agent`: A coordinator sends tasks to specialist AIs (for research, writing, or sales) and combines their answers.
- `my_parallel_agent`: Three researcher AIs run at the same time, then a final agent summarizes their results into a short executive report.

**Troubleshooting**
- Missing `GOOGLE_API_KEY`: set this environment variable or add it into a `.env` file before running an example.
- Dependency issues: ensure you installed `requirements.txt` with the correct Python version.

**License & Contribution**
Feel free to use or adapt these examples. If you want help turning one example into a small app, I can help.
