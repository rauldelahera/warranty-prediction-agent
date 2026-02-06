import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Define pages
home = st.Page("home.py", title="Home", icon="🏠", default=True)
warranty_agent = st.Page("pages/1_🔮_Warranty_Agent.py", title="Warranty Agent", icon="🔮")

# Navigation Structure
pg = st.navigation({
    "Application": [home, warranty_agent]
})

pg.run()
