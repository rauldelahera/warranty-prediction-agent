import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import ENVIRONMENT, DEBUG

st.set_page_config(page_title="Warranty Prediction Agent", page_icon="🔮", layout="wide")

st.title("🔮 Warranty Prediction Agent")
st.subheader("AI-Powered Warranty Prediction & Analysis")

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 🚀 Overview
    An intelligent agent system that predicts vehicle warranty risks using **Machine Learning** and **Conversational AI**.
    
    This platform demonstrates:
    *   **AI Agent Development** - Google ADK-powered conversational agent
    *   **ML Integration** - BigQuery ML models for prediction
    *   **Natural Language Interface** - Chat with AI about specific vehicles
    *   **Full-Stack Engineering** - Streamlit frontend + ADK backend

    ### 🌟 Key Capabilities
    1.  **Warranty Prediction Agent**: Ask questions in natural language to analyze VINs
    2.  **Risk Assessment**: ML-powered probability scoring and cost estimation
    3.  **Tool Calling**: Autonomous decision-making for which tools to use
    """)

with col2:
    st.info("""
    **Tech Stack**  
    *   Google ADK
    *   Gemini 1.5 Flash
    *   BigQuery ML
    *   Streamlit
    
    **Portfolio Project**  
    Demonstrating AI agent architecture and enterprise ML integration
    
    **Author**  
    Raul de la Hera
    """)

st.divider()

st.success("👈 Select **Warranty Agent** from the sidebar to start chatting!")

# Hiding dev details for presentation
if DEBUG:
    with st.expander("👨‍💻 Developer Info (Debug Mode Only)"):
        st.write(f"Environment: `{ENVIRONMENT.upper()}`")
