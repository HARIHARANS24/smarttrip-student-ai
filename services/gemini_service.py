import os
import json
import time
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from utils.helpers import extract_json_from_text

class GeminiService:
    """Service for interacting with Google Gemini API."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            # Just a warning so the app can still start without the key initially
            print("WARNING: GEMINI_API_KEY is not set or is invalid.")
        
        genai.configure(api_key=api_key)
        
        # Use gemini-1.5-pro or flash based on preference
        self.model = genai.GenerativeModel('gemini-2.5-flash',
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        )

    def generate_content_with_retry(self, prompt: str, retries=3, backoff_factor=1.5):
        """Generates content with retry logic for API limits."""
        for attempt in range(retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(backoff_factor * (2 ** attempt)) # Exponential backoff
        return None

    def generate_json_structured(self, prompt: str, retries=3):
        """Generates content and attempts to parse it as JSON."""
        response_text = self.generate_content_with_retry(prompt, retries)
        if not response_text:
            return None
            
        json_str = extract_json_from_text(response_text)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}\nRaw output: {response_text}")
            raise Exception("Failed to parse AI output into valid JSON.")

    def start_chat(self, history=None):
        """Starts a chat session with history."""
        if history is None:
            history = []
        return self.model.start_chat(history=history)
