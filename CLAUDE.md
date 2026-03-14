# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-powered customer service agent for a cellphone store (cellfone.io). Built with LangGraph for graph-based workflow orchestration, LangChain for LLM integration, and OpenAI GPT-4o-mini.

## Running the Project

```bash
# Local execution with sample input
python main.py

# LangGraph API dev server (uses langgraph.json config)
langgraph dev

# Install dependencies
pip install -r requirements.txt
```

Requires a `.env` file with: `OPENAI_API_KEY`, `LANGSMITH_API_KEY`, `LANGCHAIN_TRACING_V2=true`, `LANGCHAIN_PROJECT=cellfone_io_agent`, `STORE_API_KEY` (store API base URL, e.g. `http://127.0.0.1:8000/`).

## Architecture

**Workflow**: `START → message_listener → message_categorizer → [conditional router] → subgraph → END`

The system categorizes incoming customer messages into categories (order_status, product_inquiry, policy_question, complaint, operation_request, other) and routes them to specialized subgraphs.

### Key layers

- **`src/state.py`** — `StoreState` (TypedDict) defines the shared state schema flowing through the graph. Uses `Annotated[list[AnyMessage], add_messages]` for message accumulation.
- **`src/graph/`** — Compiled LangGraph workflows. `store_graph.py` is the main orchestrator; `orders_graph.py` and `support_graph.py` are subgraphs compiled as nodes.
- **`src/nodes/`** — Graph node functions with signature `state: StoreState → StoreState`. Registered in `NODES` dict in `__init__.py`.
- **`src/agents/`** — LLM chains (prompt → model → structured output). Registered in `AGENT_REGISTRY` dict in `__init__.py`.
- **`src/prompts/`** — Prompt templates split into agent role prompts (`agents.py`) and task instructions (`tasks.py`), composed together in `__init__.py`.
- **`src/nodes/tools/`** — LangChain `@tool`-decorated functions (e.g., `get_orders` calls the store API).
- **`src/data/`** — Knowledge base files (`products.txt`, `policies.txt`) for RAG/context.

### Patterns

- **Registry pattern**: Agents (`AGENT_REGISTRY`) and nodes (`NODES`) use dicts for centralized lookup.
- **Structured output**: Message categorizer uses `with_structured_output` with Pydantic models (`CategorizerMessageOutput`).
- **Tool-calling loop**: Orders subgraph uses `ToolNode` + `tools_condition` for LLM-driven tool execution cycles.
- **Subgraph composition**: Specialized workflows are compiled and added as nodes to the main graph.

## Code Style

- Use comments sparingly. Only comment complex code.

## Deployment

`langgraph.json` configures the LangGraph API deployment. The entry point is `store_graph` from `./src/graph/store_graph.py:store_graph`.
