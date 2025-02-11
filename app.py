from flask import Flask, request, jsonify, render_template
import google.generativeai as genai # Import the GenerativeAI module from the Google API
import yfinance as yf # Import the yfinance module to fetch live market data
from dotenv import load_dotenv # Import the load_dotenv function from the dotenv module
import os # Import the os module to access environment variables

load_dotenv(dotenv_path="KEY.env")  # Load the environment variables from the KEY.env file

api_key = os.getenv("API_KEY")  # Get the API key from the environment variables

genai.configure(api_key="api_key")# Configure the Gemini API with your API key

app = Flask(__name__)

def chat_with_gemini(prompt):
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text.strip()

@app.route('/')
def index():
    # Render the main HTML page
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the AJAX POST request
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Get the response from Gemini
    response_text = chat_with_gemini(user_input)
    return jsonify({"response": response_text})

@app.route('/api/market-data', methods=['GET'])
def market_data():
    # Fetch live market data
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

if __name__ == '__main__':
    app.run(debug=True)

