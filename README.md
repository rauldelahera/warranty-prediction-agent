# 🔮 Warranty Prediction Agent

**AI-powered vehicle warranty prediction using Google ADK, Gemini, and BigQuery ML**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Google ADK](https://img.shields.io/badge/Google_ADK-4285F4?style=flat&logo=google&logoColor=white)](https://google.github.io/adk-docs/)
[![Gemini](https://img.shields.io/badge/Gemini_1.5-8E75B2?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)

An intelligent conversational agent that predicts vehicle warranty claims through natural language interaction. Built to demonstrate enterprise AI agent architecture, LLM integration, and ML deployment patterns.

---

## 🎯 Overview

This platform showcases an end-to-end AI agent system where users can chat naturally about vehicles and receive ML-powered warranty predictions. The agent autonomously decides which tools to call based on conversation context.

**Example Interaction:**

```
👤 User: "What's the warranty risk for VIN 1HGCM82633A123456?"

🤖 Agent:
Warranty Prediction for VIN 1HGCM82633A123456

Prediction: Warranty claim likely
Probability: 68.3% chance of claim
Risk Level: MEDIUM RISK

Recommendation: Standard quality checks recommended.
Estimated Cost: $2,450 ± $380
```

**Key Features:**
- 💬 **Natural Language Interface** - Ask questions in plain English
- 🤖 **Autonomous Decision Making** - Agent chooses appropriate tools
- 📊 **ML-Powered Predictions** - BigQuery ML models for classification & regression
- 🔄 **Graceful Degradation** - Works even when ML services unavailable
- ⚡ **Real-time Streaming** - Live response generation

---

## 🏗️ Architecture

```
┌─────────────────┐
│   User Query    │  "What's the warranty risk for VIN ...?"
│  (Natural Lang) │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Streamlit UI   │  Chat interface
│   (Frontend)    │
└────────┬────────┘
         │
         v
┌─────────────────┐
│   ADK Agent     │  Gemini-powered intelligence
│  (Orchestrator) │  • Understands intent
└────────┬────────┘  • Selects tools
         │           • Formats response
         v
┌─────────────────┐
│ Python Tools    │  Business logic
│  (tools.py)     │  • predict_warranty_cost(vin)
└────────┬────────┘  • predict_warranty_total_cost(vin)
         │
         v
┌─────────────────┐
│  BigQuery ML    │  Machine learning models
│   (Inference)   │  • Classification (will it claim?)
└─────────────────┘  • Regression (how much?)
```

**Technology Stack:**

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | Chat UI & visualization |
| **AI Agent** | Google ADK + Gemini 1.5 Flash | Natural language understanding & orchestration |
| **Tools** | Python Functions | Prediction logic & data retrieval |
| **ML Platform** | BigQuery ML | Model training & inference |
| **Cloud** | Google Cloud Platform | Infrastructure & APIs |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+ 
- [Free Gemini API Key](https://aistudio.google.com/app/apikey) (15 req/min, 1M tokens/day)
- (Optional) Google Cloud account for BigQuery ML

### Installation

```bash
# 1. Clone repository
git clone https://github.com/rauldelahera/warranty-prediction-agent.git
cd warranty-prediction-agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure Gemini API
export GEMINI_API_KEY="your-api-key-here"

# Optional: Configure BigQuery (for full ML functionality)
export GCP_PROJECT_ID="your-gcp-project-id"

# 5. Run application
streamlit run tools/app.py
```

Open your browser to [http://localhost:8501](http://localhost:8501) 🎉

**Note:** The chat interface works immediately with just the Gemini API key. BigQuery is optional for the ML prediction features.

---

## 📁 Project Structure

```
warranty-prediction-agent/
│
├── agent_host_frontend/           # ADK Agent Configuration
│   ├── __init__.py
│   └── agent.py                   # Agent logic, system prompts, tool registration
│
├── tools/                         # Streamlit Application
│   ├── app.py                     # Main entry point
│   ├── home.py                    # Landing page
│   ├── llm_service.py             # Gemini API wrapper
│   ├── tools.py                   # Agent tool functions (predictions)
│   ├── bigquery_service.py        # BigQuery client & queries
│   └── pages/
│       └── 1_🔮_Warranty_Agent.py # Chat interface page
│
├── config.py                      # Centralized configuration
├── requirements.txt               # Python dependencies
├── QUICK_REFERENCE.py            # Developer command reference
└── README.md                      # This file
```

---

## 🧠 How It Works

### 1. User Interaction
User asks a question in natural language through the Streamlit chat interface.

### 2. Agent Processing
The ADK agent (powered by Gemini 1.5 Flash):
- Parses natural language to understand intent
- Decides autonomously which tool to call (if any)
- Extracts and formats parameters (e.g., VIN number)

### 3. Tool Execution
Python functions in `tools/tools.py` execute business logic:
```python
def predict_warranty_cost(vin: str) -> str:
    """Predict warranty claim probability for a specific vehicle VIN."""
    # Validates VIN format
    # Queries BigQuery ML model
    # Formats response
```

### 4. ML Model Inference
Tools query BigQuery ML models via SQL:
```sql
SELECT predicted_has_warranty_claim, predicted_probability
FROM ML.PREDICT(
  MODEL `warranty_models.claim_occurrence_model`,
  (SELECT * FROM `training_data` WHERE vin = '...')
)
```

### 5. Response Generation
Agent formats ML results into conversational response and streams back to user.

---

## 🎓 What This Demonstrates

This portfolio project showcases production-ready skills:

| **Skill** | **Implementation** |
|-----------|-------------------|
| **AI Agent Development** | Google ADK framework with autonomous tool calling |
| **LLM Integration** | Gemini API for natural language understanding |
| **Tool Orchestration** | Agent decides which Python functions to call |
| **ML Model Deployment** | BigQuery ML models in production workflows |
| **Full-Stack Engineering** | Backend (ADK agent) + Frontend (Streamlit) |
| **Cloud Architecture** | GCP services integration (BigQuery, AI APIs) |
| **Error Handling** | Graceful degradation when services unavailable |
| **API Design** | Clean interfaces between agent and tools |
| **Configuration Management** | Environment-based config for dev/prod |

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file or set in your shell:

```bash
# Required: Gemini API Key
GEMINI_API_KEY="your-api-key-from-google-ai-studio"

# Optional: GCP Project for BigQuery ML
GCP_PROJECT_ID="your-gcp-project-id"

# Optional: Proxy settings (if behind corporate firewall)
HTTP_PROXY="http://proxy.example.com:8080"
HTTPS_PROXY="http://proxy.example.com:8080"
```

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy and set: `export GEMINI_API_KEY="your-key"`

**Free tier:** 15 requests/minute, 1 million tokens/day (plenty for development and demos)

---

## 🛠️ Development

### Adding New Tools

The agent can be extended with new capabilities:

**1. Define tool function in `tools/tools.py`:**
```python
def your_new_tool(parameter: str) -> str:
    """Brief description for the AI agent.
    
    The agent will read this docstring to understand when to use this tool.
    """
    result = your_logic(parameter)
    return f"Result: {result}"
```

**2. Register in `agent_host_frontend/agent.py`:**
```python
from tools.tools import predict_warranty_cost, your_new_tool

root_agent = Agent(
    model=model,
    tools=[predict_warranty_cost, your_new_tool],  # Add here
    system_instruction="...",
)
```

The agent automatically learns when to use your tool based on its description!

### Running in Development Mode

```bash
# Standard mode (Streamlit only)
streamlit run tools/app.py

# Full ADK development server (advanced)
# Terminal 1:
adk web --port 8080

# Terminal 2:
cd tools && streamlit run app.py
```

---

##  Author

**Raul de la Hera**

- 💼 LinkedIn: [raul-de-la-hera](https://www.linkedin.com/in/raul-de-la-hera-712360197/)
- 💻 GitHub: [@rauldelahera](https://github.com/rauldelahera)

---

<div align="center">

**Built with:** Google ADK · Gemini 1.5 Flash · BigQuery ML · Streamlit · Python

*Personal project inspired by real-world automotive industry challenges*

</div>
