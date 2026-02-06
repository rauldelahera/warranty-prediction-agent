
import streamlit as st
import asyncio
import sys
from pathlib import Path
import logging
import json
import re

# Add project root to sys.path to find agent_host_frontend
# We are in tools/pages/
# Parent is tools/
# Parent.Parent is project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_host_frontend.agent import root_agent
from google.adk.runners import InMemoryRunner
from google.genai import types

# Runtime patch to force proper tool usage without modifying agent.py
if "CRITICAL INSTRUCTION Override" not in root_agent.instruction:
    root_agent.instruction += """

CRITICAL INSTRUCTION Override:
- You must perform tool calls using the native function calling protocol.
- DO NOT output a JSON list of tool calls as text.
- DO NOT write ["{\\"name\\": ...}"].
- Execute the tool directly by generating a tool call.
"""

def clean_adk_response(text: str) -> str:
    """Cleans up the ADK response, verifying json or boxed formatting."""
    if not text:
        return text
        
    # 1. Handle \boxed{...} format common in reasoning models
    boxed_match = re.search(r'\\boxed\{(.*)\}', text, re.DOTALL)
    if boxed_match:
        content = boxed_match.group(1)
        # It might be a quoted string containing JSON: "{\"result\": ...}"
        # Or just raw JSON: {"result": ...}
        
        # Try to unquote if it's a string literal
        if content.startswith('"') and content.endswith('"'):
            try:
                # Use json.loads to unescape the string
                content = json.loads(content)
            except json.JSONDecodeError:
                pass
        
        # Now try to parse as JSON object
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                 # Look for common result keys
                 for key in ['result', 'answer', 'content']:
                     if key in data:
                         return str(data[key])
        except json.JSONDecodeError:
            pass
            
        # If parsing failed, just return the content inside boxed
        return content

    # 2. Handle "The final answer is:" prefix
    text = text.replace("The final answer is:", "").strip()
    
    # 3. Handle Generic JSON strings in text
    if text.strip().startswith('{') and text.strip().endswith('}'):
        try:
            data = json.loads(text)
            if isinstance(data, dict):
                 if 'result' in data:
                     return str(data['result'])
        except json.JSONDecodeError:
            pass
            
    return text.replace("\\n", "\n")

st.set_page_config(page_title="Warranty Agent", page_icon="🤖", layout="wide")

st.title("🔮 Warranty Intelligence Agent")
st.markdown("Ask questions about specific VINs to predict warranty risks and estimated costs.")
st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize ADK Runner
# keeping it in session state to persist conversation (memory)
if "adk_runner" not in st.session_state:
    try:
        st.session_state.adk_runner = InMemoryRunner(agent=root_agent)
        st.session_state.session_id = "streamlit_session_v1"
        st.session_state.user_id = "streamlit_user"
        st.success("ADK Agent Initialized Successfully")
    except Exception as e:
        st.error(f"Failed to initialize ADK Agent: {e}")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask the ADK Agent..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        status_placeholder = st.empty() # Placeholder for tool status
        full_response = ""
        
        # Async function to communicate with ADK
        async def get_adk_response():
            runner = st.session_state.adk_runner
            text_response = ""
            
            # Let's ensure session exists using get_session (or create)
            session_service = runner.session_service
            session = await session_service.get_session(
                app_name=runner.app_name, 
                user_id=st.session_state.user_id, 
                session_id=st.session_state.session_id
            )
            if not session:
                await session_service.create_session(
                    app_name=runner.app_name,
                    user_id=st.session_state.user_id,
                    session_id=st.session_state.session_id
                )

            events = runner.run_async(
                user_id=st.session_state.user_id,
                session_id=st.session_state.session_id,
                new_message=types.UserContent(parts=[types.Part(text=prompt)])
            )
            
            status_placeholder.text("🤔 Thinking...")
            
            async for event in events:
                # Check for tool calls
                if event.content:
                    for part in event.content.parts:
                        if part.function_call:
                            tool_name = part.function_call.name
                            # Convert args to string if possible for display
                            args = part.function_call.args
                            status_placeholder.info(f"🛠️ Calling tool: `{tool_name}` with `{args}`")

                # Capture messages from both 'model' and the agent itself (e.g. 'root_agent')
                # Filter out tool calls/responses if only final text is desired
                if (event.author == 'model' or event.author == runner.agent.name) and event.content:
                    for part in event.content.parts:
                        if part.text:
                            text_response += part.text
            
            status_placeholder.empty() # Clear status when done
            cleaned_response = clean_adk_response(text_response)
            return cleaned_response

        try:
            # Run the async loop - use existing event loop if available
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            full_response = loop.run_until_complete(get_adk_response())
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error communicating with agent: {e}")
            logging.error(e, exc_info=True)
            # print(asdf)
