import logging
import os
import time
from typing import Dict

# Import shared configuration
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API, ENVIRONMENT

from google.adk.agents.llm_agent import Agent
from google.adk.models import Gemini
from google.adk.tools import BaseTool, ToolContext

from tools.tools import predict_warranty_cost, predict_warranty_total_cost

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Track the last tool call to prevent agent loops (not user re-queries)
_last_tool_call = {"name": None, "vin": None, "timestamp": 0}

# Configure Gemini API
if not GEMINI_API["api_key"]:
    log.error("GEMINI_API_KEY environment variable not set!")
    log.error("Get your free API key at: https://aistudio.google.com/app/apikey")
    log.error("Then set it: export GEMINI_API_KEY='your-key-here'")
    raise ValueError("GEMINI_API_KEY not configured")

log.info(f"Successfully configured Gemini in {ENVIRONMENT} environment")

# Configure the Gemini model using ADK's native Gemini support
model = Gemini(
    model_name=GEMINI_API["model"],  # gemini-1.5-flash
    api_key=GEMINI_API["api_key"],
)


# Callback function that runs BEFORE each tool is executed
# This is useful for logging, debugging, or validation
def tool_call(tool: BaseTool, args: Dict[str,any], tool_context: ToolContext):
    """Called automatically before the agent executes any tool"""
    print(f"Agent is calling tool: {tool.name} with args: {args}")
    
    # Prevent agent loops (consecutive duplicate calls within 3 seconds)
    if tool.name == "predict_warranty_cost":
        vin = args.get('vin', '').strip().upper()
        current_time = time.time()
        
        # Check if this is the same call within 3 seconds (agent looping)
        time_since_last_call = current_time - _last_tool_call["timestamp"]
        if (_last_tool_call["name"] == tool.name and 
            _last_tool_call["vin"] == vin and 
            time_since_last_call < 3):
            raise RuntimeError(f"STOP: Just called predict_warranty_cost for VIN {vin} {time_since_last_call:.1f}s ago. Do not call again. Present the previous results.")
        
        # Update the last call tracker
        _last_tool_call["name"] = tool.name
        _last_tool_call["vin"] = vin
        _last_tool_call["timestamp"] = current_time
        print(f"Allowing call for VIN {vin}")


# Create the root agent - this is the main AI agent
root_agent = Agent(
    model=model,  # The Gemini model for understanding and reasoning
    name='root_agent',  # Agent identifier
    description='A specialist for vehicle warranty prediction.',  # What the agent does
    instruction='''
You are an expert Warranty Prediction specialist with TWO capabilities:

1. WARRANTY PREDICTION (ML Model) - Predict warranty claim risk for specific vehicles
2. TOTAL COST ESTIMATION (ML Model) - Estimate total warranty claim cost for specific vehicles

=== WARRANTY PREDICTION TOOL ===
- predict_warranty_cost(vin): Predict warranty claim probability for a specific vehicle VIN using ML model.


=== TOTAL COST ESTIMATION TOOL ===
- predict_warranty_total_cost(vin): Predict warranty claim total cost for a specific vehicle VIN using ML model.

CRITICAL RULES:
- Call the tools ONLY ONCE per VIN
- After receiving prediction results, present them to the user and STOP
- Do NOT retry or call the tool multiple times with the same VIN
- If the tool returns an error, report it to the user and ask for clarification - do not retry automatically
- Once you have prediction results, your task is complete


IMPORTANT: Do not retry failed queries multiple times. Try once, report results or errors, and stop.
''',  # How to behave
    before_tool_callback=[tool_call],  # Functions to run before each tool call
    tools=[
        # Warranty prediction ML model
        predict_warranty_cost,
        predict_warranty_total_cost
    ]
)
