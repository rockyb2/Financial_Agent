from smolagents import CodeAgent, Tool, InferenceClientModel, DuckDuckGoSearchTool, tool
import gradio as gr
import os
import dotenv
from huggingface_hub import login
import yfinance as yf
from mistralai import Mistral
from langfuse import Langfuse  # ✅ Import correct


# Charger les variables d'environnement
dotenv.load_dotenv()
hf_token = os.getenv("API_KEY")
login(token=hf_token)
#memoir simple de conversation
conversation_history = []

# Initialiser Langfuse avec les nouvelles clés
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    base_url=os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")
)

agent = None

# ---------------------- OUTILS ---------------------- #
@tool
def get_realtime_price(symbol: str) -> str:
    """
    Retourne le prix en temps réel d'une action via Alpha Vantage.
    
    Args:
        symbol (str): Le symbole de l'action en bourse (ex: "AAPL", "TSLA", "MSFT").
    """
    import requests, os

    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }
    r = requests.get(url, params=params).json()

    if "Global Quote" not in r:
        return "Erreur : symbole introuvable."

    q = r["Global Quote"]
    return (
        f"Prix actuel de {symbol}: {q['05. price']} USD\n"
        f"Variation: {q['10. change percent']}"
    )

@tool
def get_stock_price(ticker: str) -> str:
    """
    Récupère le prix actuel d'une action via Yahoo Finance.

    Args:
        ticker (str): Le symbole de l'action en bourse (ex: "AAPL", "TSLA", "MSFT").
    """
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        currency = stock.info.get("currency", "USD")
        return f"Le prix actuel de {ticker} est de {price:.2f} {currency}"
    except Exception as e:
        return f"Erreur : {e}"

@tool
def get_rsi(symbol: str) -> str:
    """
    Retourne le RSI (Relative Strength Index) d'une action via Alpha Vantage.
    
    Args:
        symbol (str): Le symbole de l'action en bourse (ex: "AAPL", "TSLA", "MSFT").
    """
    import requests, os

    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "RSI",
        "symbol": symbol,
        "interval": "daily",
        "time_period": 14,
        "series_type": "close",
        "apikey": api_key
    }
    r = requests.get(url, params=params).json()

    if "Technical Analysis: RSI" not in r:
        return "Erreur : impossible de récupérer le RSI."

    last_date, last_value = next(iter(r["Technical Analysis: RSI"].items()))

    return f"RSI de {symbol} au {last_date}: {last_value['RSI']}"

@tool
def get_macd(symbol: str) -> str:
    """
    Retourne le MACD d'une action.
    
    Args:
        symbol (str): Le symbole de l'action en bourse (ex: "AAPL", "TSLA", "MSFT").
    """
    import requests, os

    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "MACD",
        "symbol": symbol,
        "interval": "daily",
        "series_type": "close",
        "apikey": api_key
    }
    r = requests.get(url, params=params).json()

    if "Technical Analysis: MACD" not in r:
        return "Erreur : MACD non disponible."

    last_date, last_value = next(iter(r["Technical Analysis: MACD"].items()))

    return (
        f"MACD de {symbol} au {last_date} :\n"
        f"- MACD : {last_value['MACD']}\n"
        f"- Signal : {last_value['MACD_Signal']}\n"
        f"- Histogramme : {last_value['MACD_Hist']}"
    )


@tool
def get_forex_rate(pair: str) -> str:
    """
    Retourne le taux de change (ex: EUR/USD).
    
    Args:
        pair (str): La paire de devises au format "BASE/QUOTE" (ex: "EUR/USD", "GBP/JPY").
    """
    import requests, os

    base, quote = pair.split("/")

    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": base,
        "to_currency": quote,
        "apikey": api_key
    }
    r = requests.get(url, params=params).json()

    try:
        rate = r["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        return f"Taux {pair} : {rate}"
    except:
        return "Erreur : paire forex invalide."


@tool
def get_stock_history(symbol: str) -> str:
    """
    Retourne l'historique journalier d'une action.
    Args:
        symbol (str): Le symbole de l'action en bourse (ex: "AAPL", "TSLA", "MSFT").
    """
    import requests, os

    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key
    }
    r = requests.get(url, params=params).json()

    if "Time Series (Daily)" not in r:
        return "Erreur : données historiques introuvables."

    last_date, last_data = next(iter(r["Time Series (Daily)"].items()))

    return (
        f"Dernier jour disponible : {last_date}\n"
        f"Ouverture : {last_data['1. open']}\n"
        f"Clôture : {last_data['4. close']}\n"
        f"Haut : {last_data['2. high']}\n"
        f"Bas : {last_data['3. low']}"
    )

# ---------------------- AGENT ---------------------- #
def build_agent():
    global agent
    agent = CodeAgent(
        model=InferenceClientModel(),
        tools=[
            get_stock_price, 
            DuckDuckGoSearchTool(), 
            get_rsi, 
            get_macd, 
            get_forex_rate, 
            get_realtime_price, 
            get_stock_history
        ],
    )
    return agent

def chat_with_agent(message, history):
    global agent, conversation_history
    if agent is None:
        agent = build_agent()
    
    context_text = ""
    for msg in conversation_history:
        role = msg["role"]
        content = msg["content"]
        context_text += f"{role}: {content}\n"
    
    full_prompt = context_text + f"user: {message}\nassistant:"
    
    # ---------------------- Langfuse modern ---------------------- #
    # Crée un "span" pour suivre l'interaction utilisateur → agent
    with langfuse.start_as_current_observation(as_type="span", name="agent_chat") as obs:
        obs.update(input={"user_message": message})          # Envoie le message utilisateur
        output = str(agent.run(full_prompt))                     # Exécute l'agent
        obs.update(output={"agent_response": output})       # Envoie la réponse de l'agent
    
    # Mise à jour de la mémoire
    conversation_history.append({"role": "user", "content": message})
    conversation_history.append({"role": "assistant", "content": output})
    return output

# ---------------------- GRADIO ---------------------- #
gr.ChatInterface(
    fn=chat_with_agent,
    title="Agent IA Finance",
    description="Agent IA expert en analyse boursière avec suivi Langfuse.",
    type="messages"
).launch()