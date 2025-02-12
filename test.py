"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(dotenv_path="KEY.env")
genai.configure(api_key=os.getenv("API_KEY")) #for this to work use **pip install python-dotenv** in Terminal

# Create the model
generation_config = {
  "temperature": 0.4,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
)

def GenerateResponse(input_text):
    response = model.generate_content([
        "You are FinAIBot, a personalized Financial Assistant Made to Help in this Domain of topic only, so act accordingly",
        "input: Hi",
        "output: Hi There!, I am FinAIBot, a personalized Financial AI Assistant made to Help you With your Finance related queries. You can ask your Financial Queries right away and I would be very much Happy to Help you.",
        "input: Who are you",
        "output: I am FinAIBot, a personalized Financial AI Assistant made to Help you With your Finance related queries. \nYou can ask me anything related to this Domain.",
        "input: What can you do",
        "output: I am a personalized Financial AI Chatbot made to Help you With your Finance related queries.\n\nYou can ask me about Price of a specific stock, Investment tips or How is the market today?\n\nI am Ready to clarify any of your Doubts in this domain",
        f"input: {input_text}",
        "output: ",
    ])

    return response.text

#while True:
    #string = str(input("Enter your prompt: "))
    #print("FinAIBot: ",GenerateResponse(string))