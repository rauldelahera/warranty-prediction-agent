
import asyncio
import sys
from pathlib import Path
import logging

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Setup logging
logging.basicConfig(level=logging.ERROR)

from agent_host_frontend.agent import root_agent
from google.adk.runners import InMemoryRunner
from google.genai import types

async def debug_chat():
    print("Initializing InMemoryRunner...")
    runner = InMemoryRunner(agent=root_agent)
    
    user_id = "debug_user"
    session_id = "debug_session"
    
    # Ensure session
    session = await runner.session_service.create_session(
        app_name=runner.app_name, 
        user_id=user_id, 
        session_id=session_id
    )
    
    message_text = "Hello, who are you? Please answer briefly."
    print(f"Sending: {message_text}")
    
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=types.UserContent(parts=[types.Part(text=message_text)])
    )
    
    print("\n--- Events Stream ---")
    async for event in events:
        print(f"Event ID: {event.id}")
        print(f"  Author: {event.author}")
        print(f"  Type: {type(event)}")
        if event.content:
            print(f"  Content present: Yes")
            for part in event.content.parts:
                print(f"    Part Text: {part.text}")
        else:
            print(f"  Content present: No")
        print("-" * 20)

if __name__ == "__main__":
    asyncio.run(debug_chat())
