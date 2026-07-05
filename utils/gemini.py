import google.generativeai as genai
import os

# Configure Gemini API with secure API key loading
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")

genai.configure(api_key=api_key)

# Create reusable Gemini client
model = genai.GenerativeModel("gemini-1.5-flash")

def test_connection():
    """
    Test the Gemini API connection by sending a simple "Hello" message.
    Returns the response from the model.
    """
    try:
        response = model.generate_content("Hello")
        return response.text
    except Exception as e:
        raise Exception(f"Gemini API connection test failed: {str(e)}")

def optimize_prompt(prompt):
    """
    Optimize a prompt using Gemini AI.
    
    Args:
        prompt (str): The original prompt to optimize
        
    Returns:
        str: The optimized prompt
        
    Raises:
        Exception: If the optimization fails
    """
    try:
        optimization_instruction = f"""
        You are an expert prompt engineer. Your task is to optimize the following prompt for better AI responses.
        
        Original Prompt: {prompt}
        
        Please rewrite the prompt to:
        1. Be more specific and clear
        2. Include necessary context
        3. Specify the desired output format
        4. Add relevant constraints or guidelines
        5. Make it more actionable
        
        Return ONLY the optimized prompt, without any additional explanation or commentary.
        """
        
        response = model.generate_content(optimization_instruction)
        optimized_prompt = response.text.strip()
        return optimized_prompt
    except Exception as e:
        raise Exception(f"Failed to optimize prompt with Gemini: {str(e)}")
