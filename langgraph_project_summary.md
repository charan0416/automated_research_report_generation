# Automated Research Report Generation with LangGraph

## Project Overview

This project leverages LangGraph to create an autonomous agent system for generating comprehensive research reports. It automates the process of generating AI analyst personas, conducting simulated interviews with these analysts, performing web research, and compiling the findings into a structured report. The system is designed to be highly modular, stateful, and capable of human-in-the-loop interaction.

Key features include:
- **Dynamic Analyst Persona Generation**: Creates AI analysts with specific roles and focuses based on a given topic and feedback.
- **Parallel Interview Process**: Conducts multiple analyst interviews concurrently using LangGraph's parallel execution capabilities.
- **Web Research Integration**: Incorporates real-time information retrieval through web search during interviews.
- **Human-in-the-Loop Feedback**: Allows for human intervention to guide the research process and refine analyst outputs.
- **Structured Report Generation**: Compiles an introduction, detailed content from analyst insights, and a conclusion into a final report, with source citations.
- **Flexible Output Formats**: Saves reports in both DOCX and PDF formats.

## LangGraph Concepts in Project

This project leverages the following LangGraph libraries and concepts:

*   **`langgraph.graph.StateGraph`**: Used to define the core workflow as a stateful graph, orchestrating the entire report generation and individual interview processes.
*   **`langgraph.checkpoint.memory.MemorySaver`**: Enables checkpointing, allowing the graph's state to be saved and restored. This is crucial for human-in-the-loop interactions and resuming interrupted workflows.
*   **`langgraph.types.Send`**: Facilitates parallel execution of sub-workflows, specifically for running multiple analyst interviews concurrently.

**Important Learning Topics from this Project:**

*   **State Management**: How to define and update a shared state (`TypedDict`, `Annotated` with `operator.add`) across complex, multi-step workflows.
*   **Graph Construction**: Building agentic workflows using nodes (individual actions) and edges (transitions) to control the flow.
*   **Conditional Routing**: Implementing dynamic decision-making within the graph to alter workflow paths based on specific conditions (e.g., human feedback).
*   **Subgraphs for Modularity**: Creating reusable nested graphs (`build_interview_graph`) to manage complexity and promote code reusability.
*   **Parallel Processing**: Leveraging `Send` to execute multiple tasks simultaneously, improving efficiency.
*   **Human-in-the-Loop**: Designing workflows that incorporate human intervention and feedback using checkpointing and interruption points.
*   **Integration with LLMs and Tools**: Seamlessly integrating Large Language Models (LLMs) for content generation and external tools (like web search) for information retrieval.

## Architecture

The project's architecture is built around a multi-agent system orchestrated by LangGraph, integrating various libraries for specific functionalities:

*   **LangChain**: Provides the foundational components for building LLM applications, including `HumanMessage`, `SystemMessage`, `AIMessage` for structured communication, and `TavilySearchResults` for web search.
*   **FastAPI**: Used to build the web API that serves the autonomous report generation functionality, providing endpoints for initiating reports, submitting feedback, and downloading results.
*   **Pydantic**: Essential for defining data models (e.g., `Analyst`, `Perspectives`, `SearchQuery`, and the various `State` objects like `ResearchGraphState`, `InterviewState`). It ensures data validation and clear structure within the application.
*   **python-dotenv**: Manages environment variables, loading API keys and configurations from `.env` files.
*   **python-docx**: Used for generating and saving reports in DOCX format.
*   **ReportLab**: Utilized for generating and saving reports in PDF format.
*   **SQLAlchemy**: (Although not directly shown in the `workflow.py`, `report_routes.py` indicates its use in `db_config.py` for database interactions, likely for user authentication or report storage metadata). This ORM helps manage database operations.
*   **Jinja2Templates**: Powers the templating for the FastAPI application's HTML responses, rendering dynamic content for the user interface.
*   **`logging`**: For robust logging throughout the application to monitor execution and debug issues.
