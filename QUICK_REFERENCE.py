"""
🔮 Warranty Intelligence Platform - Quick Reference
===================================================

Portfolio project demonstrating AI agent architecture and ML integration
Author: Raul de la Hera
Tech Stack: Google ADK · Gemini · BigQuery ML · Streamlit

"""

# ==============================================================================
# SETUP & INSTALLATION
# ==============================================================================

"""
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export GEMINI_API_KEY="your-api-key"
export GCP_PROJECT_ID="your-project-id"  # Optional
"""

# ==============================================================================
# RUNNING THE APPLICATION
# ==============================================================================

"""
# Method 1: Streamlit UI Only (Recommended)
streamlit run tools/app.py

# Method 2: Full ADK Development
# Terminal 1:
adk web --port 8080

# Terminal 2:
cd tools && streamlit run app.py

# Access at:
http://localhost:8501
"""

# ==============================================================================
# PROJECT STRUCTURE
# ==============================================================================

PROJECT_STRUCTURE = """
warranty-intelligence-platform/
├── agent_host_frontend/
│   ├── agent.py              # ADK agent logic & tool registration
│   └── __init__.py
│
├── tools/
│   ├── app.py                # Streamlit entry point
│   ├── home.py               # Landing page
│   ├── llm_service.py        # Gemini API wrapper
│   ├── tools.py              # Agent tool functions (predictions)
│   ├── bigquery_service.py   # BigQuery client
│   └── pages/
│       └── 1_🔮_Warranty_Agent.py  # Chat interface
│
├── config.py                 # Configuration & env variables
├── requirements.txt          # Python dependencies
├── QUICK_REFERENCE.py        # This file
└── README.md                 # Full documentation
"""

# ==============================================================================
# DEVELOPMENT WORKFLOW
# ==============================================================================

"""
# Install new packages
pip install package-name
pip freeze > requirements.txt

# Run in debug mode (shows extra info)
# Config sets DEBUG=True automatically when running locally

# Kill Streamlit server
pkill -f streamlit

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Check for import errors
python -c "import agent_host_frontend.agent; print('✓ Imports OK')"
"""

# ==============================================================================
# GEMINI API CONFIGURATION
# ==============================================================================

"""
# Get API Key:
1. Visit https://aistudio.google.com/app/apikey
2. Create API key
3. Set in environment:
   export GEMINI_API_KEY="AIza..."

# Free Tier Limits:
- 15 requests per minute
- 1 million tokens per day
- Sufficient for development & demos

# Model Configuration (in config.py):
GEMINI_API = {
    "model": "gemini-1.5-flash",  # Fast, efficient model
    "api_key": os.getenv("GEMINI_API_KEY"),
}
"""

# ==============================================================================
# BIGQUERY ML (OPTIONAL)
# ==============================================================================

"""
# Required BigQuery Resources:
1. GCP project with BigQuery enabled
2. ML models:
   - warranty_models.claim_occurrence_model (classification)
   - warranty_models.total_cost_model (regression)
3. Training data tables

# Note: The chat works WITHOUT BigQuery!
# The agent handles errors gracefully and still demonstrates
# conversational AI capabilities.

# Configure BigQuery:
export GCP_PROJECT_ID="your-gcp-project-id"

# Update in config.py:
BIGQUERY = {
    "project": os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
}
"""

# ==============================================================================
# ADDING NEW AGENT TOOLS
# ==============================================================================

"""
# Step 1: Define tool in tools/tools.py
def your_new_tool(param: str) -> str:
    '''
    Clear description for the AI agent.
    Explain what this tool does and when to use it.
    '''
    result = some_logic(param)
    return f"Result: {result}"

# Step 2: Register in agent_host_frontend/agent.py
from tools.tools import your_new_tool

root_agent = Agent(
    model=model,
    tools=[
        predict_warranty_cost,
        predict_warranty_total_cost,
        your_new_tool,  # Add here
    ],
    system_instruction="...",
)

# The agent automatically learns when to use your tool!
"""

# ==============================================================================
# USEFUL COMMANDS
# ==============================================================================

COMMANDS = {
    "Start app": "streamlit run tools/app.py",
    "Stop app": "pkill -f streamlit or Ctrl+C",
    "Activate venv": "source venv/bin/activate",
    "Install deps": "pip install -r requirements.txt",
    "Check API key": "echo $GEMINI_API_KEY",
    "Clear cache": "find . -name __pycache__ -exec rm -rf {} +",
    "Test imports": "python -c 'from agent_host_frontend import agent'",
}

# ==============================================================================
# TROUBLESHOOTING
# ==============================================================================

TROUBLESHOOTING = """
Issue: "GEMINI_API_KEY not configured"
Fix: export GEMINI_API_KEY="your-key"

Issue: "Module not found"
Fix: 
  1. source venv/bin/activate
  2. pip install -r requirements.txt

Issue: BigQuery errors
Expected: Agent handles gracefully with error message
Fix (optional): Set GCP_PROJECT_ID and create ML models

Issue: Pylance import warnings
Why: google-adk has no type stubs
Fix: Warnings are cosmetic - code runs fine!
"""

# ==============================================================================
# PORTFOLIO NOTES
# ==============================================================================

"""
What This Project Demonstrates:
--------------------------------
✓ AI Agent Development (Google ADK)
✓ LLM Integration (Gemini API)
✓ Tool Calling & Orchestration
✓ ML Model Integration (BigQuery ML)
✓ Full-Stack Engineering (Python + Streamlit)
✓ Cloud Architecture (GCP)
✓ Error Handling & Graceful Degradation
✓ Configuration Management

Key Files to Show Recruiters:
-----------------------------
1. README.md - Full project overview
2. agent_host_frontend/agent.py - Agent logic
3. tools/tools.py - Tool implementations
4. config.py - Clean configuration pattern

Tech Stack:
-----------
- Google ADK: Agent framework
- Gemini 1.5 Flash: LLM for NLU
- BigQuery ML: ML model hosting
- Streamlit: Frontend framework
- Python 3.12+: Backend language
"""

# ==============================================================================
# DOCUMENTATION LINKS
# ==============================================================================

DOCS = {
    "Google ADK": "https://google.github.io/adk-docs/",
    "Gemini API": "https://ai.google.dev/docs",
    "BigQuery ML": "https://cloud.google.com/bigquery/docs/bqml-introduction",
    "Streamlit": "https://docs.streamlit.io/",
    "Full README": "README.md",
}

if __name__ == "__main__":
    print("🔮 Warranty Intelligence Platform")
    print("=" * 50)
    print("\n📚 Quick Reference Guide")
    print("\nCommon Commands:")
    for cmd, desc in COMMANDS.items():
        print(f"  • {cmd}: {desc}")
    
    print("\n📖 Documentation:")
    for name, url in DOCS.items():
        print(f"  • {name}: {url}")
    
    print("\n✨ Tech Stack: Google ADK · Gemini · BigQuery ML · Streamlit")
    print("\nFor full documentation, see README.md")


