# weather-mcp-server

A production-ready [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server built in Python. This service acts as a bridge between Large Language Models (LLMs) and external APIs, allowing AI agents to securely fetch real-time weather data and provide instructions to analyze it for EV fleet operations.

## 🎯 Overview

LLMs are constrained by their training data cutoffs. This server provides the "hands" (Tools) and the "workflow instructions" (Prompts) an AI needs to interact with the live physical world. Specifically, it enables an AI assistant to fetch current weather conditions.

### Core Capabilities

* **Action Execution (Tools):** Exposes a `get_current_weather` tool that strictly validates AI-provided coordinates and fetches live data from the Open-Meteo API.
* **Workflow Templating (Prompts):** Exposes an `analyze_fleet_weather` prompt that injects dynamic context and strict analytical guidelines into the LLM's system instructions.
* **Hallucination Defense:** Utilizes `Pydantic` for strict, runtime validation of all LLM inputs before executing backend logic.

## 🏗️ Architecture

1.  **Client:** An MCP-compatible host (e.g., Claude Desktop or the MCP Inspector).
2.  **Transport Layer:** JSON-RPC over Standard Input/Output (`stdio`).
3.  **Server:** Python `FastMCP` application managing asynchronous execution (`asyncio`) and network requests (`httpx`).
4.  **Data Source:** Open-Meteo API (No authentication required).

## ⚙️ Prerequisites

* Python 3.10 or higher
* Node.js and `npx` (for running the local MCP Inspector)

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/26042000jayesh/mcp-weather-agent.git](https://github.com/26042000jayesh/mcp-weather-agent.git)
   cd mcp-weather-agent
   ```

2. **Create and activate a virtual environment:**

   *On macOS/Linux:*
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   *On Windows:*
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install mcp httpx pydantic
   ```

4. **Testing Locally (MCP Inspector):**
   ```bash
   npx @modelcontextprotocol/inspector python server.py
   ```
