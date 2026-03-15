# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (streams a test message through the graph)
python main.py

# Run LangGraph API server (enables LangGraph Studio UI)
langgraph dev
```

No test framework is configured yet.

## Architecture

AI-powered customer service agent for a cellphone store, built with **LangGraph** and **OpenAI GPT-4o-mini**. Classifies incoming customer messages and routes them to specialized subgraphs.

### Data Flow

```
START → [msg_cleanup] → [message_listener] → [message_categorizer] → [router]
                                                                          ├─ "operation_request" → orders_subgraph → END
                                                                          └─ other → END
```

### State (`src/state.py`)

`StoreState` is the single shared object flowing through all nodes:
- `messages`: Full conversation history (reduced with `add_messages`)
- `last_message`: Most recent message string, extracted by `message_listener`
- `message_category`: Classified intent string, set by `message_categorizer`
- `orders`: List populated by the orders subgraph after tool execution

### Key Patterns

**Node pattern**: Every node is a pure function `(StoreState) -> dict` returning only the state keys it updates.

**Categorizer** (`src/agents/message_categorizer.py`): A LangChain chain using `with_structured_output(CategorizerMessageOutput)` to enforce typed classification into 6 categories defined in `src/structured_outputs.py`.

**Orders subgraph** (`src/graph/orders_graph.py`): Implements the agentic tool-calling loop — LLM decides to call `get_orders` → `ToolNode` executes it → `process_results` parses and saves to state → loop repeats until LLM signals done.

**Message cleanup** (`src/nodes/message_cleanup.py`): Runs at graph start, keeps only the last 5 messages using `RemoveMessage`.

### Adding a New Category

1. Add enum value to `MessageCategory` in `src/structured_outputs.py`
2. Create a subgraph in `src/graph/`
3. Add a routing branch in the conditional router in `src/graph/store_graph.py`

### Environment Variables

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | OpenAI authentication |
| `STORE_API_KEY` | Base URL for the store REST API (default: `http://127.0.0.1:8000/`) |
| `LANGSMITH_API_KEY` | LangSmith tracing (optional) |
| `LANGCHAIN_TRACING_V2` | Enable LangSmith tracing |

### Deployment

`langgraph.json` maps `store_graph` to `./src/graph/store_graph.py:store_graph` for the LangGraph API server.
