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

## 🚀 Try It Live

**Live Demo:** [https://warranty-agent-1023331849991.us-central1.run.app](https://warranty-agent-1023331849991.us-central1.run.app)

<!-- Optional: Add screenshot here
![Warranty Agent Demo](docs/screenshot.png)
-->

No installation required! Try asking:
- *"What's the warranty risk for VIN 1HGBH41JXMN100001?"*
- *"Predict both probability and cost"*
- *"What's the claim likelihood for VIN 1HGBH41JXMN100334?"*

---

## 🎓 What This Demonstrates

This portfolio project showcases production-ready skills:

| **Skill** | **Implementation** |
|-----------|-------------------|
| **AI Agent Development** | Google ADK framework with autonomous tool calling |
| **LLM Integration** | Gemini API for natural language understanding |
| **Tool Orchestration** | Agent decides which Python functions to call |
| **ML Model Deployment** | BigQuery ML models in production workflows |
| **Cloud Architecture** | Cloud Run serverless deployment |
| **Secret Management** | GCP Secret Manager for API keys |
| **Containerization** | Docker + Cloud Build for CI/CD |
| **Full-Stack Engineering** | Backend (ADK agent) + Frontend (Streamlit) |
| **Infrastructure as Code** | Dockerfile, SQL scripts, gcloud configurations |
| **Error Handling** | Graceful degradation when services unavailable |
| **API Design** | Clean interfaces between agent and tools |
| **Configuration Management** | Environment-based config for dev/prod |
| **DevOps** | Automated builds, deployments, and secret injection |

---

## ☁️ Deploy Your Own

<details>
<summary><b>Click to expand: Full Cloud Deployment Guide</b></summary>

This project is deployed on **Google Cloud Platform** using serverless architecture:

### Architecture

```
┌─────────────────┐
│   Cloud Run     │  Containerized Streamlit app
│   (Serverless)  │  Auto-scaling, HTTPS, managed
└────────┬────────┘
         │
         ├──────────► Secret Manager (Gemini API Key)
         ├──────────► BigQuery ML (Prediction models)
         └──────────► Container Registry (Docker images)
```

### Prerequisites

- Google Cloud account with billing enabled
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed
- Docker (for local builds) or Cloud Build access

### One-Time Setup

#### 1. Create GCP Project

```bash
# Create project
gcloud projects create YOUR-PROJECT-ID --name="Warranty Prediction Agent"

# Set as active project
gcloud config set project YOUR-PROJECT-ID

# Enable billing (required for Cloud Run)
# Visit: https://console.cloud.google.com/billing/linkedaccount?project=YOUR-PROJECT-ID
```

#### 2. Enable Required APIs

```bash
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  secretmanager.googleapis.com \
  bigquery.googleapis.com
```

#### 3. Store Gemini API Key in Secret Manager

```bash
# Create secret with your Gemini API key
echo -n "YOUR_GEMINI_API_KEY" | gcloud secrets create gemini-api-key \
  --data-file=- \
  --replication-policy="automatic"

# Grant Cloud Run access to the secret
PROJECT_NUMBER=$(gcloud projects describe YOUR-PROJECT-ID --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding gemini-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

#### 4. Setup BigQuery ML Models

```bash
# Create datasets
bq mk --project_id=YOUR-PROJECT-ID --location=US --dataset warranty_data
bq mk --project_id=YOUR-PROJECT-ID --location=US --dataset warranty_models

# Run setup script to create sample data and train models
bq query --project_id=YOUR-PROJECT-ID --use_legacy_sql=false < setup_bigquery.sql
```

This creates:
- **1,000 sample vehicle records** for training
- **Classification model** (predicts warranty claim probability)
- **Regression model** (predicts warranty claim cost)

### Deploy to Cloud Run

#### Option 1: Using Cloud Build (Recommended)

```bash
# Build container image
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/warranty-agent

# Deploy to Cloud Run
gcloud run deploy warranty-agent \
  --image gcr.io/YOUR-PROJECT-ID/warranty-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GCP_PROJECT_ID=YOUR-PROJECT-ID" \
  --set-secrets "GEMINI_API_KEY=gemini-api-key:latest" \
  --memory 1Gi \
  --timeout 300
```

#### Option 2: Using Local Docker

```bash
# Build locally
docker build -t gcr.io/YOUR-PROJECT-ID/warranty-agent .

# Push to Container Registry
docker push gcr.io/YOUR-PROJECT-ID/warranty-agent

# Deploy (same as above)
gcloud run deploy warranty-agent \
  --image gcr.io/YOUR-PROJECT-ID/warranty-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GCP_PROJECT_ID=YOUR-PROJECT-ID" \
  --set-secrets "GEMINI_API_KEY=gemini-api-key:latest" \
  --memory 1Gi \
  --timeout 300
```

### Verify Deployment

```bash
# Check service status
gcloud run services describe warranty-agent --region us-central1

# View logs
gcloud run services logs read warranty-agent --region us-central1 --limit=50

# Get service URL
gcloud run services describe warranty-agent --region us-central1 --format='value(status.url)'
```

### Cost Estimate

With free tier limits, expected monthly cost: **$0-2**

- **Cloud Build:** First 120 build-minutes/day free
- **Cloud Run:** 2M requests/month free, 360k GB-seconds memory free
- **BigQuery:** 1 TB queries/month free, 10 GB storage free
- **Secret Manager:** First 6 secret accesses free

### Update Deployment

After making code changes:

```bash
# Rebuild and redeploy
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/warranty-agent && \
gcloud run deploy warranty-agent \
  --image gcr.io/YOUR-PROJECT-ID/warranty-agent \
  --platform managed \
  --region us-central1
```
</details>

---

## 💻 Local Development

<details>
<summary><b>Click to expand: Run locally for development</b></summary>

### Prerequisites

- Python 3.12+
- [Free Gemini API Key](https://aistudio.google.com/app/apikey)
- Google Cloud account with BigQuery access (required for predictions)

### Setup

```bash
# 1. Clone repository
git clone https://github.com/rauldelahera/warranty-prediction-agent.git
cd warranty-prediction-agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
export GEMINI_API_KEY="your-gemini-api-key"
export GCP_PROJECT_ID="your-gcp-project-id"

# 5. Authenticate with Google Cloud
gcloud auth application-default login

# 6. Run application
streamlit run tools/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Adding New Agent Tools

**1. Define tool in `tools/tools.py`:**
```python
def your_new_tool(parameter: str) -> str:
    """Brief description - the agent reads this to understand when to use it."""
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

The agent automatically learns when to use your tool based on its docstring!

</details>


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
├── Dockerfile                     # Container image definition
├── .dockerignore                  # Docker build exclusions
├── setup_bigquery.sql             # BigQuery dataset & model setup
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

##  Author

**Raul de la Hera**

- 💼 LinkedIn: [raul-de-la-hera](https://www.linkedin.com/in/raul-de-la-hera-712360197/)
- 💻 GitHub: [@rauldelahera](https://github.com/rauldelahera)

---

<div align="center">

**Built with:** Google ADK · Gemini 1.5 Flash · BigQuery ML · Streamlit · Python

*Personal project inspired by real-world automotive industry challenges*

</div>
