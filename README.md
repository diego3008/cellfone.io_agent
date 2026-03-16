# Cellfone.io Agent

An AI-powered customer service agent for cellphone store operations, built with **LangGraph** and **OpenAI GPT-4o-mini**. The agent processes incoming customer messages, classifies them by intent, and routes them to specialized workflows for handling orders, product inquiries, complaints, and more.

## Overview

The agent uses a graph-based workflow to:

1. **Listen** — capture the latest incoming customer message
2. **Categorize** — classify the message intent using an LLM
3. **Route** — dispatch to the appropriate subgraph based on category
4. **Act** — execute domain-specific logic (e.g., fetch orders from the store API)

## Architecture

### Main Graph

```
Customer Message
       │
       ▼
[msg_cleanup]             → Trims conversation history to the last 5 messages
       │
       ▼
[message_listener]        → Extracts the last message string into last_message
       │
       ▼
[message_categorizer]     → GPT-4o-mini classifies intent → message_category (list)
       │
       ▼
[Conditional Router]      → Fan-out: dispatches to one or more subgraphs in parallel
       │
       ├── "order_inquiry"   → [Orders Subgraph]   ─┐
       ├── "product_inquiry" → [Products Subgraph] ──┤→ (parallel) → END
       └── no matching category → END
```

The router supports **parallel subgraph execution**: if a message matches multiple categories (e.g. both `order_inquiry` and `product_inquiry`), both subgraphs are fanned out simultaneously using `Send` and their results are merged back into state.

### Orders Subgraph

Implements an agentic tool-calling loop to fetch store data:

```
[fetch_orders]  ←─────────────────────────────────┐
       │  (LLM agent with bound tools)              │
       ▼                                            │
 tools_condition                                    │
       │                                            │
       ├── tool call needed → [tools]               │
       │                    (get_orders /            │
       │                     get_products)           │
       │                          │                 │
       │                          ▼                 │
       │                  [process_results] ────────┘
       │                  (parses JSON, writes
       │                   orders / products to state)
       │
       └── done → END
```

### Message Categories

| Category | Description |
|---|---|
| `order_inquiry` | Customer asking about an existing order → Orders Subgraph |
| `product_inquiry` | Questions about products, features, or availability → Products Subgraph |
| `policy_question` | Questions about store policies, returns, warranties |
| `complaint` | Customer dissatisfaction or issue reports |
| `other` | Unrelated or unclassifiable messages |

> Multiple categories can be returned at once, triggering parallel subgraph execution.

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
    │   ├── message_cleanup.py      # Trims history to last 5 messages
    │   ├── message_listener.py     # Extracts last message from state
    │   ├── message_categorizer.py  # Runs categorizer, updates state
    │   ├── orders_nodes.py         # Orders agent with tool-calling loop
    │   └── tools/
    │       └── orders_tools.py     # Tools: get_orders, get_products (store API)
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
    products: list[any]
    support_answer: str
```

### Message Cleanup

Runs at the start of every graph invocation. Uses `RemoveMessage` to delete the oldest messages when the conversation history exceeds 5 messages, keeping the context window lean.

### Message Categorization

The `message_categorizer` node runs a LangChain chain: `PromptTemplate` → `ChatOpenAI(gpt-4o-mini)` → `with_structured_output(CategorizerMessageOutput)`. This enforces a typed `MessageCategory` enum value on every response with no free-form output.

### Orders Subgraph

Activated when the category is `operation_request`. An LLM agent is bound to two tools:

- **`get_orders`** — GET `{STORE_API_KEY}api/orders/` → returns the current order list
- **`get_products`** — GET `{STORE_API_KEY}api/products/` → returns the product catalog

The agent loops (LLM → ToolNode → `process_results`) until it signals it is done. `process_results` inspects the last `ToolMessage`, parses the JSON payload, and writes the results into `orders` or `products` on the state.

## Roadmap

- [ ] Subgraphs for `product_inquiry`, `complaint`, and `policy_question` categories
- [ ] Customer feedback handling
- [ ] Memory/conversation history support
- [ ] Integration with a full store backend
- [ ] Human-in-the-loop escalation for unresolved complaints
