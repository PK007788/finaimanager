"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import google.generativeai as genai
import yfinance as yf
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

# Dictionary mapping company names to their stock tickers
company_to_ticker = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "amazon": "AMZN",
    "facebook": "META",
    "tesla": "TSLA",
    # Add more companies and their tickers as needed
}

def get_stock_price(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="1d")
    if not data.empty:
        latest_price = data["Close"].iloc[-1]
        return f"The latest price of {stock_symbol} is ${latest_price:.2f}"
    else:
        return f"Could not retrieve data for {stock_symbol}"

def GenerateResponse(input_text):
    # Check if the input is a stock price query
    if "price of" in input_text.lower():
        company_name = input_text.split("price of")[-1].strip().lower()
        stock_symbol = company_to_ticker.get(company_name)
        if stock_symbol:
            return get_stock_price(stock_symbol)
        else:
            return f"Could not find the stock ticker for {company_name}"
    
    # Generate response using Gemini model
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

# Uncomment the following lines to test the chatbot in a loop
#while True:
    #string = str(input("Enter your prompt: "))
    #print("FinAIBot: ", GenerateResponse(string))