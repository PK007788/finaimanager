from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import yfinance as yf
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Check if API key is loaded
if not api_key:
    raise ValueError("API_KEY not found! Ensure it's set in the .env file.")

# Configure Gemini AI API
genai.configure(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Function to get response from Gemini AI
def chat_with_gemini(prompt):
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text.strip()

# Route to serve React frontend
@app.route("/")
def index():
    return render_template("index.html")

# Chatbot API endpoint
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response_text = chat_with_gemini(user_input)
    return jsonify({"response": response_text})

# Market data API endpoint
@app.route("/api/market-data", methods=["GET"])
def market_data():
    tickers = {
        "Sensex": "^BSESN",
        "Nifty": "^NSEI",
        "Gold": "GC=F",
        "Silver": "SI=F",
        "USD/INR": "INR=X"
    }

    market_info = {}
    for name, symbol in tickers.items():
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if not data.empty:
            latest_price = data["Close"].iloc[-1]
            prev_close = data["Close"].iloc[-2] if len(data) > 1 else latest_price
            change = latest_price - prev_close
            percent_change = (change / prev_close) * 100 if prev_close else 0

            market_info[name] = {
                "price": round(latest_price, 2),
                "change": round(change, 2),
                "percent_change": round(percent_change, 2)
            }
        else:
            market_info[name] = {"error": "No data available"}

    return jsonify(market_info)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

