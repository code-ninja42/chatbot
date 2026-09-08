import os
import time
import requests

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

load_dotenv()


# =========================================================
# LIVE BACKEND URL
# =========================================================

API_BASE_URL = "https://chatbot-project-pro5.onrender.com"


# =========================================================
# PRODUCT TOOL
# =========================================================

@tool
def get_products():
    """
    Get all products from the store.

    Use this tool for:
    - product names
    - product prices
    - product stock
    - product availability
    - cheapest products
    - most expensive products
    - shoes
    - clothing
    - electronics
    - accessories
    """

    response = requests.get(
        f"{API_BASE_URL}/products",
        timeout=30
    )

    response.raise_for_status()

    return response.text


# =========================================================
# ORDER TOOL
# =========================================================

@tool
def get_orders():
    """
    Get all orders from the store.

    Use this tool for:
    - order information
    - order status
    - delivery status
    - tracking information
    - customer order information
    """

    response = requests.get(
        f"{API_BASE_URL}/orders",
        timeout=30
    )

    response.raise_for_status()

    return response.text


# =========================================================
# GEMINI MODEL
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
    max_retries=3
)


# =========================================================
# LANGCHAIN AGENT
# =========================================================

agent = create_agent(
    model=llm,

    tools=[
        get_products,
        get_orders
    ],

    system_prompt="""
You are a helpful store assistant.

Your job is ONLY to help users with information related
to this store.

==================================================
STORE INFORMATION YOU CAN HANDLE
==================================================

PRODUCTS:
- Product names
- Product prices
- Product stock
- Product availability
- Cheapest product
- Most expensive product
- Products by category
- Product comparisons
- Shoes
- Clothing
- Electronics
- Accessories
- Other store products

ORDERS:
- Order information
- Order ID
- Customer name
- Order status
- Delivery status
- Tracking number
- Order quantity
- Order total

==================================================
IMPORTANT TOOL RULES
==================================================

1. For ANY question about products, ALWAYS use get_products.

2. For ANY question about price, ALWAYS use get_products.

3. For ANY question about stock, ALWAYS use get_products.

4. For ANY question about availability, ALWAYS use get_products.

5. For cheapest or most expensive products,
   ALWAYS use get_products.

6. For ANY question about orders, ALWAYS use get_orders.

7. For order status, ALWAYS use get_orders.

8. For delivery status, ALWAYS use get_orders.

9. For tracking information, ALWAYS use get_orders.

10. If the user provides an order ID, find that order
    in the result returned by get_orders.

11. If the user provides a customer name and order ID,
    verify both using get_orders.

12. NEVER invent product information.

13. NEVER invent order information.

14. NEVER guess prices, stock, availability, order status,
    delivery status, or tracking numbers.

15. Only use the actual information returned by the
    store tools when answering store-data questions.

==================================================
OUTSIDE QUESTIONS
==================================================

You ONLY have information about this store.

If the user asks about something unrelated to the store,
do NOT answer the unrelated question.

Instead say:

"Sorry, I can only help with information related to this store."

Examples of unrelated questions:
- General knowledge
- Coding questions
- Python questions
- News
- Movies
- Sports
- Politics
- Personal advice
- General science
- General mathematics
- Questions about other companies
- Questions about people

==================================================
GREETINGS
==================================================

Simple greetings are allowed.

For example:

User: Hello
Assistant: Hello! 👋 How can I help you with our store?

User: Hi
Assistant: Hi! 👋 What would you like to know about our store?

Do NOT call a store tool for a simple greeting.

==================================================
ANSWER STYLE
==================================================

- Be clear.
- Be concise.
- Use natural language.
- Do not show technical details.
- Do not mention tools unless necessary.
- Do not mention LangChain or Gemini to the customer.
- Use actual store data when answering store questions.
"""
)


# =========================================================
# CHAT FUNCTION
# =========================================================

def ask_chatbot(question):

    last_error = None

    for attempt in range(3):

        try:

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

        except Exception as e:

            last_error = e

            print(
                f"Gemini attempt {attempt + 1} failed: {e}"
            )

            if attempt < 2:
                time.sleep(3)

    raise last_error