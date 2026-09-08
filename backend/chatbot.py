import requests
import os

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

load_dotenv()

API_BASE_URL = "https://chatbot-project-pro5.onrender.com"


# =========================================
# TOOL 1: GET PRODUCTS
# =========================================

@tool
def get_products():
    """Get all products from the store including price, stock and availability."""

    response = requests.get(
        f"{API_BASE_URL}/products",
        timeout=30
    )

    response.raise_for_status()

    return response.json()


# =========================================
# TOOL 2: GET ORDERS
# =========================================

@tool
def get_orders():
    """Get all orders including customer name, order ID, status and tracking information."""

    response = requests.get(
        f"{API_BASE_URL}/orders",
        timeout=30
    )

    response.raise_for_status()

    return response.json()


# =========================================
# GEMINI MODEL
# =========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)


# =========================================
# LANGCHAIN AGENT
# =========================================

agent = create_agent(
    model=llm,
    tools=[
        get_products,
        get_orders
    ],
    system_prompt="""
You are a helpful store assistant.

You can help users with:

1. Products
2. Product prices
3. Product stock
4. Product availability
5. Cheapest products
6. Most expensive products
7. Orders
8. Order status
9. Delivery status
10. Tracking information

IMPORTANT:

- Use the available tools whenever the user asks about real store data.
- Do not invent product or order information.
- For product questions, use get_products.
- For order questions, use get_orders.
- If the user provides an order ID, find that order from the tool result.
- Answer clearly and naturally.
- Keep answers concise.
"""
)


# =========================================
# CHAT FUNCTION
# =========================================

def ask_chatbot(question):

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    return response["messages"][-1].content