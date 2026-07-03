import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY", "YOUR_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def optimize_prompt(prompt):
    response = model.generate_content(
        f"""
        Improve this prompt.
        Make it detailed.
        Add context.
        Add expected output.

        Prompt:
        {prompt}
        """
    )

    return response.text
