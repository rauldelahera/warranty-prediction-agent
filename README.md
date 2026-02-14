# 🔮 Warranty Prediction Agent

**AI-powered vehicle warranty prediction using Google ADK, Gemini, and BigQuery ML**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Google ADK](https://img.shields.io/badge/Google_ADK-4285F4?style=flat&logo=google&logoColor=white)](https://google.github.io/adk-docs/)
[![Gemini](https://img.shields.io/badge/Gemini_1.5-8E75B2?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)

An intelligent conversational agent that predicts vehicle warranty claims through natural language interaction. Ask questions like *"What's the warranty risk for VIN 1HGCM82633A123456?"* and get ML-powered predictions with probability scores and cost estimates.

Built to demonstrate AI agent architecture, LLM integration, BigQuery ML, and serverless deployment on Google Cloud.

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

**Live Demo:** [https://warranty-agent-ptowuhxy5q-uc.a.run.app](https://warranty-agent-ptowuhxy5q-uc.a.run.app)

<!-- Optional: Add screenshot here
![Warranty Agent Demo](docs/screenshot.png)
-->

No installation required! Try asking:
- *"What's the warranty risk for VIN 1HGBH41JXMN100001?"*
- *"Predict both probability and cost"*
- *"What's the claim likelihood for VIN 1HGBH41JXMN100334?"*

---

## 🎓 What This Demonstrates

This portfolio project showcases:

**AI & ML Engineering:**
- **AI Agent Development** - Google ADK framework with autonomous tool calling
- **LLM Integration** - Gemini 1.5 Flash API for natural language understanding
- **ML Model Training** - BigQuery ML with SQL (logistic regression + linear regression)
- **ML Deployment** - Production ML inference integrated into conversational agent

**Cloud & DevOps:**
- **Serverless Architecture** - Cloud Run with auto-scaling and managed infrastructure
- **Secret Management** - GCP Secret Manager for secure API key handling
- **Containerization** - Docker + Cloud Build for automated deployments
- **Infrastructure as Code** - SQL scripts, Dockerfiles, and gcloud configurations

**Full-Stack Development:**
- **Backend** - Python functions integrated with AI agent for business logic
- **Frontend** - Streamlit chat UI with real-time response streaming

---

## 📊 Machine Learning Models

This project uses **BigQuery ML** to train and deploy models entirely with SQL:

**Model 1: Warranty Claim Classification**
```sql
CREATE OR REPLACE MODEL `warranty_models.claim_occurrence_model`
OPTIONS(model_type='logistic_reg', input_label_cols=['has_warranty_claim'])
AS SELECT model_year, make, vehicle_type, mileage, state, has_warranty_claim
FROM `warranty_data.training_data`;
```
- **Type:** Logistic Regression
- **Purpose:** Predicts probability of warranty claim (binary classification)
- **Output:** Probability score (0-100%) + risk level

**Model 2: Claim Cost Prediction**
```sql
CREATE OR REPLACE MODEL `warranty_models.total_cost_model`
OPTIONS(model_type='linear_reg', input_label_cols=['total_claim_cost'])
AS SELECT model_year, make, vehicle_type, mileage, state, total_claim_cost
FROM `warranty_data.training_data` WHERE has_warranty_claim = TRUE;
```
- **Type:** Linear Regression
- **Purpose:** Estimates total warranty claim cost
- **Output:** Dollar amount prediction

**Training Data:**
- 1,000 synthetic vehicle records generated for demonstration
- Features: VIN, make, model year, vehicle type, mileage, state
- Labels: warranty claim occurrence (binary) and claim cost (continuous)
- Created via SQL with `GENERATE_ARRAY` and randomization functions

> **Note:** This is a portfolio/proof-of-concept project using synthetic data. In production, you'd train on real historical warranty claims data with proper data governance and compliance

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

## 🧠 How It Works

User asks a question in natural language → Gemini-powered agent understands intent and calls the appropriate Python tool → Tool queries BigQuery ML model via SQL → Agent formats ML predictions into conversational response → Streamed back to user in real-time.

See the [Architecture](#🏗️-architecture) diagram above for the complete flow.

<details>
<summary><b>Click to expand: Project Structure</b></summary>

```
warranty-prediction-agent/
├── agent_host_frontend/agent.py   # ADK agent config, system prompts
├── tools/
│   ├── app.py                     # Streamlit entry point
│   ├── tools.py                   # ML prediction functions
│   ├── bigquery_service.py        # BigQuery client
│   └── pages/1_🔮_Warranty_Agent.py  # Chat UI
├── config.py                      # Environment configuration
├── setup_bigquery.sql             # ML model training script
├── Dockerfile                     # Container definition
└── requirements.txt               # Python dependencies
```

</details>

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
