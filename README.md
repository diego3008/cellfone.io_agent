# Cellfone.io Agent

An AI-powered customer service agent for cellphone store operations, built with **LangGraph** and **OpenAI GPT-4o-mini**. The agent processes incoming customer messages, classifies them by intent, and routes them to specialized workflows for handling orders, product inquiries, complaints, and more.

## Overview

The agent uses a graph-based workflow to:

1. **Listen** — capture the latest incoming customer message
2. **Categorize** — classify the message intent using an LLM
3. **Route** — dispatch to the appropriate subgraph based on category
4. **Act** — execute domain-specific logic (e.g., fetch orders from the store API)

## Architecture

```
Customer Message
       │
       ▼
[message_listener]        → Extracts the last message from state
       │
       ▼
[message_categorizer]     → GPT-4o-mini classifies the message intent
       │
       ▼
[Conditional Router]      → Routes based on message_category
       │
       ├── order_status   → [Orders Subgraph] → tool calls → store API
       ├── product_inquiry → (planned)
       ├── policy_question → (planned)
       ├── complaint       → (planned)
       └── other          → END
```

### Message Categories

| Category | Description |
|---|---|
| `order_status` | Customer asking about an existing order |
| `product_inquiry` | Questions about products, features, or availability |
| `policy_question` | Questions about store policies, returns, warranties |
| `complaint` | Customer dissatisfaction or issue reports |
| `operation_request` | Internal operational requests |
| `other` | Unrelated or unclassifiable messages |

## Project Structure

```
cellfone_io_agent/
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── langgraph.json               # LangGraph deployment config
├── .env                         # Environment variables (not committed)
└── src/
    ├── state.py                 # Shared state schema (StoreState)
    ├── structured_outputs.py    # Pydantic models for LLM outputs
    ├── agents/
    │   └── message_categorizer.py  # Categorizer agent chain
    ├── nodes/
    │   ├── message_listener.py     # Extracts last message from state
    │   ├── message_categorizer.py  # Runs categorizer, updates state
    │   ├── orders_nodes.py         # Orders node with tool-calling LLM
    │   └── tools/
    │       └── orders_tools.py     # Tool: get_orders (calls store API)
    ├── graph/
    │   ├── store_graph.py          # Main workflow graph
    │   └── orders_graph.py         # Orders subgraph
    └── prompts/
        ├── agents.py               # Agent role/system prompts
        └── tasks.py                # Task-specific prompt templates
```

## Tech Stack

- **[LangGraph](https://github.com/langchain-ai/langgraph)** — graph-based agent orchestration
- **[LangChain](https://github.com/langchain-ai/langchain)** — LLM framework and utilities
- **[OpenAI GPT-4o-mini](https://platform.openai.com/docs/models)** — language model for categorization and tool-calling
- **[Pydantic](https://docs.pydantic.dev/)** — structured output validation
- **[LangSmith](https://smith.langchain.com/)** — tracing and observability

## Setup

### Prerequisites

- Python 3.11+
- An OpenAI API key
- (Optional) A LangSmith API key for tracing
- A running local store API at `http://127.0.0.1:8000/` (for order tools)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd cellfone_io_agent

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key

# Optional: LangSmith tracing
LANGSMITH_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=cellfone_io_agent

# Local store API base URL
STORE_API_KEY=http://127.0.0.1:8000/
```

## Usage

### Running Locally

```bash
python main.py
```

By default, `main.py` runs the graph with a sample message and streams node outputs to the console:

```python
initial_state = {
    "messages": ["I need to update some product records"],
    "message_category": ""
}
```

### LangGraph Studio / API

The project is configured for deployment with LangGraph's API server:

```bash
langgraph dev
```

This exposes the following graphs via the LangGraph API:

| Graph | Entry Point |
|---|---|
| `store_graph` | `src/graph/store_graph.py:store_graph` |
| `orders_graph` | `src/graph/orders_graph.py:graph` |

## How It Works

### State

All nodes share a typed state object (`StoreState`):

```python
class StoreState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    last_message: str
    message_category: str
    last_checked_order: str
    orders: list[any]
```

### Message Categorization

The categorizer uses a `PromptTemplate` + `ChatOpenAI` + `with_structured_output` pipeline to enforce a `CategorizerMessageOutput` Pydantic model as the LLM response, guaranteeing a valid `MessageCategory` enum value every time.

### Orders Subgraph

When a message is classified as `order_status`, the orders subgraph activates an LLM with bound tools. The `get_orders` tool makes a GET request to the store API and returns the current order list.

## Roadmap

- [ ] Subgraphs for `product_inquiry`, `complaint`, and `policy_question` categories
- [ ] Customer feedback handling
- [ ] Memory/conversation history support
- [ ] Integration with a full store backend
- [ ] Human-in-the-loop escalation for unresolved complaints
