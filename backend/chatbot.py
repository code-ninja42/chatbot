import os
import requests

from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://chatbot-project-pro5.onrender.com"
)


@tool
def get_products():
    """
    Get all products from the store.

    Use this when the user asks about:
    products, prices, stock, categories, or availability.
    """
    response = requests.get(
        f"{API_BASE_URL}/products",
        timeout=30
    )

    response.raise_for_status()

    return response.json()


@tool
def get_orders():
    """
    Get all orders from the store.

    Use this when the user asks about:
    orders, order status, customers, or tracking information.
    """
    response = requests.get(
        f"{API_BASE_URL}/orders",
        timeout=30
    )

    response.raise_for_status()

    return response.json()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


tools = [
    get_products,
    get_orders
]


agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are a helpful store chatbot.

You have access to product and order information.

RULES:

1. For questions about products, prices, stock,
   categories, or availability, use get_products.

2. For questions about orders, order status,
   customers, or tracking, use get_orders.

3. Always use the appropriate tool when the answer
   requires store database information.

4. Never invent product or order information.

5. If the requested information is not present
   in the tool result, say:
   "I don't have that information."

6. When comparing products, examine all products
   returned by get_products.

7. For questions such as:
   - highest price
   - lowest price
   - highest stock
   - lowest stock
   - most expensive product
   - cheapest product

   examine ALL products returned by get_products
   before answering.

8. For questions about unavailable products,
   check the availability field from get_products.

9. For questions about cancelled orders,
   check the status field from get_orders.

10. Give short and clear answers.

11. Do not show tool calls or technical details
    to the user.

12. If the user says something casual such as
    "hi", "hello", or "hii", respond normally
    without using a tool.
"""
)


def ask_chatbot(question):

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })

    content = result["messages"][-1].content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if item.get("type") == "text":
                    text_parts.append(
                        item.get("text", "")
                    )

            elif isinstance(item, str):
                text_parts.append(item)

        return "".join(text_parts).strip()

    return str(content).strip()