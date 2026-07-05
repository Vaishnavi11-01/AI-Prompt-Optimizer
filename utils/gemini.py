import google.generativeai as genai
import os

# Configure Gemini API with secure API key loading
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")

genai.configure(api_key=api_key)

# Create reusable Gemini client
model = genai.GenerativeModel("gemini-1.5-flash")
