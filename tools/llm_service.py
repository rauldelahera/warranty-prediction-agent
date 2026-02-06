"""LLM Service for calling Gemini API."""
import google.generativeai as genai
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API

# Configure Gemini API
if GEMINI_API["api_key"]:
    genai.configure(api_key=GEMINI_API["api_key"])

def call_llm(prompt: str, system_message: str = "You are a helpful AI assistant.") -> str:
    """
    Call Gemini API with a prompt and return response.
    
    Args:
        prompt: User's question or request
        system_message: Optional system instruction
    
    Returns:
        LLM response as string
    """
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel(
            model_name=GEMINI_API["model"],
            system_instruction=system_message
        )
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}. Make sure GEMINI_API_KEY is set in your environment."
