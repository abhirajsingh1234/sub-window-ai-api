# Sub-Window AI Assistant

> A **Multi-Agent AI System** — a persistent, always-on-screen assistant powered by a LangChain multi-agent architecture, capable of autonomously searching the web, sending emails, sending WhatsApp messages, and scraping GitHub — all from a single natural language command.

---

## ⚠️ What Makes This a Multi-Agent System

This project is not a simple chatbot. It implements a **multi-agent architecture** where distinct, specialized AI agents collaborate to handle user requests:

| Agent Role | Responsibility |
|---|---|
| **Supervisor Agent** | Receives user input, decomposes the task, and delegates to specialized sub-agents |
| **Planner Agent** | Breaks complex requests into structured, executable steps |
| **Executor Agent** | Carries out individual steps using available tools |
| **Synthesizer Agent** | Aggregates outputs from all agents into a coherent final response |

Each agent operates independently, communicates through a shared message passing layer, and is orchestrated by LangChain's agent graph — making the system capable of reasoning across multiple hops rather than producing a single-shot response.

---

## 🛠️ Agent Capabilities — What It Can Actually Do

This is where the system goes beyond conversation. The agents are equipped with **real-world action tools** that let the assistant interact with external systems autonomously:

| Capability | Description |
|---|---|
| 🔍 **Web Search** | Agents can search the internet in real time to answer queries, fetch current information, and research topics autonomously |
| 📧 **Send Email** | Compose and dispatch emails to a specified recipient directly from a natural language instruction — no manual drafting required |
| 💬 **Send WhatsApp Message** | Send WhatsApp messages to a given phone number programmatically, enabling instant notifications or communication triggers |
| 🐙 **GitHub Scraping** | Scrape GitHub repositories, profiles, issues, or commit history to extract structured data for analysis or reporting |

### Example Interactions

```
User: "Search for the latest news on LangChain and email me a summary at abhi@example.com"
→ Search Agent fetches results → Synthesizer drafts summary → Email tool dispatches it

User: "Scrape the top 5 repos from github.com/langchain-ai and send me a WhatsApp summary"
→ GitHub Scraper collects repo data → Synthesizer formats it → WhatsApp tool delivers it

User: "Find the OpenAI pricing page and email the details to my team"
→ Web Search locates the page → Executor extracts content → Email tool sends it
```

These capabilities make the assistant a **true action-taking agent** — not just an information retriever, but a system that closes the loop by acting on the information it finds.

---

## Overview

**Sub-Window AI Assistant** is a desktop-integrated multi-agent system that lives permanently on your screen as a floating sub-window. Unlike traditional AI chat interfaces, this system deploys a **network of collaborating LangChain agents** behind a FastAPI backend, enabling it to plan, delegate, and execute multi-step tasks — all while remaining persistently visible on screen without disrupting your workflow.

This project demonstrates:

- ✅ **Multi-agent orchestration** — Supervisor–Worker agent pattern with LangChain
- ✅ **Task decomposition** — Complex queries broken into sub-tasks and routed to specialized agents
- ✅ **Agent tool use** — Agents equipped with tools to act, not just respond
- ✅ **Persistent desktop presence** — Always-on-screen overlay that surfaces agent output in real time
- ✅ **Extensible agent graph** — Designed for MCP server integration and deep agent hierarchies

---

## Key Features

- 🧠 **Multi-Agent Core** — A supervisor–worker agent network where each agent has a defined role and communicates through a structured message graph
- 🔗 **LangChain Agent Orchestration** — Built on LangChain's agent framework for reliable chain-of-thought reasoning, tool binding, and inter-agent communication
- 🔍 **Web Search** — Agents autonomously search the internet to fetch real-time information and research topics on demand
- 📧 **Email Sending** — Send emails to any specified address directly from a natural language instruction
- 💬 **WhatsApp Messaging** — Dispatch WhatsApp messages to a given phone number programmatically as part of an agent workflow
- 🐙 **GitHub Scraping** — Extract structured data from GitHub repositories, profiles, issues, and commit histories
- 🖥️ **Always-on-screen overlay** — Persists as a sub-window across all active applications; no context-switching required
- ⚡ **FastAPI Backend** — Async REST API layer that routes requests into the agent pipeline and streams responses back
- 🔧 **Modular Agent Design** — Each agent is independently defined, making it easy to add, swap, or upgrade individual agents
- 🌐 **Chrome Profile Integration** — Dedicated Chrome profile powers the sub-window UI with full browser context
- 🔮 **Future-ready** — Architecture is primed for MCP (Model Context Protocol) server integration and deep hierarchical agent workflows

---

## Multi-Agent Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Sub-Window UI                            │
│            (Always-on-screen Chrome overlay)                  │
└────────────────────────────┬─────────────────────────────────┘
                             │  HTTP Request
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                           │
│                        (run.py)                              │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│               LangChain Multi-Agent Orchestration             │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                  Supervisor Agent                    │   │
│   │       (Task intake, decomposition, delegation)       │   │
│   └──────────┬──────────────────────┬───────────────────┘   │
│              │                      │                        │
│              ▼                      ▼                        │
│   ┌──────────────────┐   ┌──────────────────────┐           │
│   │   Planner Agent  │   │    Executor Agent     │           │
│   │  (Step-by-step   │──▶│  (Tool invocation,   │           │
│   │   task planning) │   │   action execution)  │           │
│   └──────────────────┘   └──────────┬───────────┘           │
│                                     │                        │
│                          ┌──────────▼───────────────────┐    │
│                          │          Tool Layer           │    │
│                          │  🔍 Web Search                │    │
│                          │  📧 Email Sender              │    │
│                          │  💬 WhatsApp Messenger        │    │
│                          │  🐙 GitHub Scraper            │    │
│                          └──────────┬────────────────────┘    │
│                                     │                        │
│                          ┌──────────▼───────────┐           │
│                          │  Synthesizer Agent    │           │
│                          │ (Response aggregation)│           │
│                          └───────────────────────┘           │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼ Structured Response
┌──────────────────────────────────────────────────────────────┐
│                      Sub-Window UI                            │
│                  (Renders agent output)                       │
└──────────────────────────────────────────────────────────────┘
```

### How the Agents Collaborate

1. **User sends a query** via the sub-window UI
2. **Supervisor Agent** receives the query, classifies it, and decomposes it into sub-tasks
3. **Planner Agent** converts sub-tasks into a structured execution plan
4. **Executor Agent** runs each step, invoking tools where needed (search, APIs, computation)
5. **Synthesizer Agent** aggregates all step outputs into a single, coherent response
6. **FastAPI** streams the result back to the sub-window UI in real time

This pipeline means the system can handle **multi-hop reasoning tasks** — queries that require multiple steps, intermediate decisions, and tool calls — not just single-turn Q&A.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangChain (multi-agent orchestration) |
| Backend API | FastAPI (Python, async) |
| Runtime | Python 3.10+ |
| UI Layer | Chrome sub-window (profile-based overlay) |
| Inter-Agent Communication | LangChain message passing / agent graph |
| Configuration | `.env` environment management |
| Dependency Management | `requirements.txt` |

---

## Project Structure

```
sub-window-ai-api/
├── app/                  # Agent definitions, tools, API routes
│   ├── agents/           # Supervisor, Planner, Executor, Synthesizer agents
│   ├── tools/            # Tool implementations bound to agents
│   └── routes/           # FastAPI route handlers
├── chrome_profile/       # Chrome profile powering the sub-window UI
├── run.py                # Entry point — initializes agents and starts FastAPI
├── requirements.txt      # Python dependencies
├── .env                  # API keys and environment configuration
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Google Chrome installed
- An LLM API key (OpenAI, Anthropic, etc.)

### Installation

```bash
# Clone the repository
git clone https://github.com/abhirajsingh1234/sub-window-ai-api.git
cd sub-window-ai-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```env
# .env
OPENAI_API_KEY=your_api_key_here
# Add any other required keys
```

### Run

```bash
python run.py
```

The FastAPI backend starts and initializes the multi-agent pipeline. The Chrome sub-window connects to the local API and renders the assistant overlay on your screen.

---

## Roadmap

- [ ] **MCP Server Integration** — Plug Model Context Protocol servers into the agent tool layer for real-time access to external data sources and services
- [ ] **Deep Agent Hierarchies** — Expand into fully hierarchical multi-agent systems with domain-specific sub-agents (research agent, code agent, data agent)
- [ ] **LangGraph Migration** — Move agent orchestration to LangGraph for fine-grained control over agent state and transitions
- [ ] **Persistent Agent Memory** — Long-term memory across sessions for contextual continuity
- [ ] **Streaming Agent Output** — Real-time token-level streaming of each agent's reasoning to the UI
- [ ] **Agent Observability** — Trace and visualize inter-agent communication and tool calls

---

## Why This Project

Most AI assistants operate as stateless, single-turn responders. **Sub-Window AI Assistant** takes a different approach — deploying a network of specialized agents that plan, delegate, and execute collaboratively, demonstrating what production-grade agentic AI systems look like in practice.

The persistent sub-window form factor solves a real problem: AI should be immediately accessible without breaking your workflow. Together, these two ideas — multi-agent intelligence and persistent desktop presence — form the core thesis of this project.

---

## Author

**Abhi** — AI/ML Engineer at Idolize Business Solutions  
Specializing in LangChain/LangGraph multi-agent systems, RAG pipelines, and intelligent automation.

[GitHub](https://github.com/abhirajsingh1234)

---

## License

This project is open source. See the repository for license details.
