# Automated Research Report Generation with LangGraph

This project leverages LangGraph to create an autonomous agent system for generating comprehensive research reports. It automates the process of generating AI analyst personas, conducting simulated interviews with these analysts, performing web research, and compiling the findings into a structured report. The system is designed to be highly modular, stateful, and capable of human-in-the-loop interaction.

## Key Features

*   **Dynamic Analyst Persona Generation**: Creates AI analysts with specific roles and focuses based on a given topic and feedback.
*   **Parallel Interview Process**: Conducts multiple analyst interviews concurrently using LangGraph's parallel execution capabilities.
*   **Web Research Integration**: Incorporates real-time information retrieval through web search during interviews.
*   **Human-in-the-Loop Feedback**: Allows for human intervention to guide the research process and refine analyst outputs.
*   **Structured Report Generation**: Compiles an introduction, detailed content from analyst insights, and a conclusion into a final report, with source citations.
*   **Flexible Output Formats**: Saves reports in both DOCX and PDF formats.

## Setup Instructions

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository

First, clone the project repository to your local machine:

```powershell
git clone https://github.com/Venumurala91/automated-research-report-generation.git
cd automated-research-report-generation
```

### 2. Create and Activate a Python Virtual Environment

It's recommended to use a virtual environment to manage project dependencies:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1 # On Windows PowerShell
# On macOS/Linux: source env/bin/activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```powershell
pip install -r requirements.txt
```

### 4. Configure API Keys (Create `.env` file)

This project requires API keys for Large Language Models (LLMs) and web search.
Create a file named `.env` in the root directory of your project (e.g., `automated-research-report-generation/.env`) and add your API keys there.

Example `.env` file:
```dotenv
OPENAI_API_KEY="your_openai_api_key_here"
GOOGLE_API_KEY="your_google_api_key_here"
GROQ_API_KEY="your_groq_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"

# Optional: If using Astra DB for checkpointing or other storage
ASTRA_DB_API_ENDPOINT="your_astra_db_api_endpoint"
ASTRA_DB_APPLICATION_TOKEN="your_astra_db_application_token"
ASTRA_DB_KEYSPACE="your_astra_db_keyspace"

# Set the preferred LLM provider for the workflow (e.g., openai, google, groq)
LLM_PROVIDER="openai"
```
**Remember to replace the placeholder values with your actual API keys.**

## How to Run the Project

You can run the project in two main ways: executing the core workflow script or running the FastAPI web application.

### 1. Run the Main Workflow (`workflow.py`)

This will execute the entire LangGraph-based research report generation process from your terminal.

Navigate to the `research_and_analyst` directory and run the script:

```powershell
cd D:\ai_projects\mlops_project_by_sunny\automated-research-report-generation\research_and_analyst
python backend_server\workflow.py
```

The script will:
*   Generate AI analyst personas.
*   Pause for your feedback.
*   Conduct parallel interviews.
*   Compile a final report.
*   Save the report as `DOCX` and `PDF` files in the `generated_report` directory within the `research_and_analyst` folder.

### 2. Run the FastAPI Web Application

The FastAPI application provides a web interface to interact with the report generation system.

First, ensure your virtual environment is active. Then, from the project root directory (`automated-research-report-generation/`), run the Uvicorn server:

```powershell
cd D:\ai_projects\mlops_project_by_sunny\automated-research-report-generation
uvicorn research_and_analyst.api.main:app --reload
```

*   The `--reload` flag enables auto-reloading on code changes, useful for development.
*   Once the server starts, you can access the application in your web browser, typically at `http://127.0.0.1:8000`.

## Generating the Workflow Diagram (Optional)

The `workflow.py` script has commented-out code to generate a visual diagram of the LangGraph workflow. If you want to visualize the graph:

1.  **Uncomment the code**: In `research_and_analyst/backend_server/workflow.py`, uncomment the lines under `# Generate and save the Mermaid diagram` block at the end of the `if __name__ == "__main__":` section.
2.  **Install `matplotlib`**: Ensure `matplotlib` is installed: `pip install matplotlib`
3.  **Run `workflow.py`**: Execute `python backend_server\workflow.py` as described above.
4.  **View Diagram**: A `workflow_architecture.png` file will be saved in the `generated_report` directory.
