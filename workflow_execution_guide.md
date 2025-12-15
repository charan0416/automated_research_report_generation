# Workflow Execution Guide: Automated Research Report Generation

This document outlines the step-by-step execution of the `workflow.py` script and explains what happens at each stage, including the expected outputs.

## How to Run `workflow.py`

To run the main workflow, navigate to the `research_and_analyst` directory in your terminal and execute the following command:

```powershell
cd D:\ai_projects\mlops_project_by_sunny\automated-research-report-generation\research_and_analyst
python backend_server\workflow.py
```

## Step-by-Step Execution and Outputs

When you run `workflow.py`, the following sequence of events unfolds:

### Step 1: Initial Setup and Model Loading

*   **Action**: The script initializes the `ModelLoader` to load the configured LLM and embedding models. It also sets up `ApiKeyManager` to load API keys from your `.env` file.
*   **Expected Output**: You will see log messages indicating which models are being loaded and whether API keys were successfully retrieved from the environment.
    ```
    # Example log outputs (may vary slightly)
    INFO: ModelLoader: YAML config loaded (config_keys=['llm', 'embedding_model'])
    INFO: ApiKeyManager: OPENAI_API_KEY loaded from environment
    INFO: ApiKeyManager: GOOGLE_API_KEY loaded from environment
    INFO: ModelLoader: Loading LLM (provider=openai, model=gpt-4o)
    ```

### Step 2: Analyst Creation and First Interruption (Human Feedback)

*   **Action**: The `AutonomousReportGenerator`'s main LangGraph starts. The `create_analyst` node is executed, which uses the LLM to generate AI analyst personas based on the predefined topic (`"Impact of GenAI over the future Jobs?"`) and `max_analysts` (3).
*   **Interruption**: After creating analysts, the graph enters the `human_feedback` node, which is configured to `interrupt_before`. This pauses the execution and prompts you for feedback.
*   **Expected Output**: The terminal will display the details of the generated analysts, followed by a prompt for your input.
    ```
    Name: Dr. Anya Sharma
    Affiliation: Future of Work Institute
    Role: Labor Economist specializing in AI impact
    Description: Analyzes macroeconomic trends and policy implications of AI on employment.
    --------------------------------------------------
    Name: Mr. Ben Carter
    Affiliation: Tech Workforce Development Board
    Role: Skills Gap Analyst
    Description: Focuses on emerging skill requirements and retraining programs in an AI-driven economy.
    --------------------------------------------------
    Name: Ms. Chloe Kim
    Affiliation: Ethical AI & Society Lab
    Role: Socio-Technical Researcher
    Description: Investigates the societal and ethical implications of AI, particularly concerning equity and job displacement.
    --------------------------------------------------

     Enter your feedback or press Enter to continue as is: 
    ```

### Step 3: Incorporating Human Feedback (or Continuing)

*   **Action**: You provide feedback (or press Enter to continue without it). The graph's state is updated with your input.
*   **Routing**: The `initiate_all_interviews` function, connected via a conditional edge from `human_feedback`, determines the next steps. If you provided feedback that requires re-creation of analysts (e.g., specific instructions like "add something from startup perspective"), it might route back to `create_analyst`. If not, or if you press Enter, it proceeds to initiate the interviews.
*   **Expected Output**: If you provide feedback and it triggers re-creation, you'll see new analyst personas. If you continue, the process will move to the interview stage, which usually runs silently in the background initially, with no immediate output to the console for each individual interview step.

### Step 4: Parallel Execution of Interviews (Subgraphs)

*   **Action**: The `initiate_all_interviews` function uses `langgraph.types.Send` to trigger multiple `conduct_interview` subgraphs concurrently, one for each generated analyst. Each subgraph acts as an independent agent, performing the following steps:
    1.  **Ask Question**: The analyst generates a question for an "expert" based on their persona and the topic.
    2.  **Search Web**: The question is used to formulate a web search query, and `TavilySearchResults` fetches relevant information.
    3.  **Generate Answer**: An "expert" LLM generates an answer to the analyst's question, incorporating the web search context.
    4.  **Save Interview**: The conversation transcript is saved.
    5.  **Write Section**: The analyst synthesizes their findings into a section of the final report.
*   **Expected Output**: This stage runs in the background. The `stream_mode="values"` in the `graph.stream` loop in `workflow.py` (for the second stream) processes events, but you've set it to `pass` in the `for _ in graph.stream(...)` loop, so it won't print individual interview steps directly to the console. The main output visible in the terminal will be related to the final report generation once all interviews are complete.

### Step 5: Report Generation (Sections, Introduction, Conclusion)

*   **Action**: Once all parallel interviews are complete, the main graph proceeds:
    1.  `write_report`: Collects all individual sections from the analyst interviews and consolidates them into the main body of the report.
    2.  `write_introduction`: Generates an introduction based on the topic and the compiled sections.
    3.  `write_conclusion`: Generates a conclusion based on the topic and the compiled sections.
*   **Expected Output**: These steps primarily involve LLM calls and state updates, so you won't see detailed step-by-step output in the console unless explicit `print` statements are added within these functions.

### Step 6: Final Report Assembly and Saving

*   **Action**: The `finalize_report` node combines the introduction, main content, conclusion, and consolidated sources into a single `final_report` string.
*   **Saving**: The `save_report` method is called, which then uses `_save_as_docx` and `_save_as_pdf` to save the final report to the `generated_report` directory.
*   **Expected Output**: You will see confirmation messages in the terminal indicating that the reports have been saved, along with their file paths.
    ```
    # Example output
    Report Saved: D:\ai_projects\mlops_project_by_sunny\automated-research-report-generation\generated_report\Impact_of_GenAI_over_the_future_Jobs_20251203_103000.docx
    Report Saved: D:\ai_projects\mlops_project_by_sunny\automated-research-report-generation\generated_report\Impact_of_GenAI_over_the_future_Jobs_20251203_103000.pdf
    ```

## Converting this Markdown Guide to PDF

Since I cannot directly generate a PDF for you, you can use various tools to convert this `.md` file to a PDF:

1.  **VS Code Extensions**: Many VS Code extensions (e.g., "Markdown PDF") allow you to right-click on a Markdown file and export it as a PDF.
2.  **Pandoc**: A universal document converter. If you have Pandoc installed, you can use the following command in your terminal:
    ```powershell
    pandoc workflow_execution_guide.md -o workflow_execution_guide.pdf
    ```
3.  **Online Converters**: Several websites allow you to upload a Markdown file and convert it to PDF.
