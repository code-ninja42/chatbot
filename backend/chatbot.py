import requests

from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI


# Load .env
load_dotenv()


# =========================================================
# TOOL 1: PRODUCTS API
# =========================================================

@tool
def get_products():
    """
    Get all products from the store.

    Use this when the user asks about:
    products, prices, stock, categories, or availability.
    """

    response = requests.get(
        "http://127.0.0.1:8000/products"
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# TOOL 2: ORDERS API
# =========================================================

@tool
def get_orders():
    """
    Get all orders from the store.

    Use this when the user asks about:
    orders, order status, customers, or tracking information.
    """

    response = requests.get(
        "http://127.0.0.1:8000/orders"
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# GEMINI LLM
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


# =========================================================
# TOOLS
# =========================================================

tools = [
    get_products,
    get_orders
]


# =========================================================
# AGENT
# =========================================================

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

6. When comparing products, such as highest price,
   lowest price, highest stock, or lowest stock,
   examine the complete product data returned
   by get_products.

7. Give a short, clear answer to the user.

8. Do not show tool calls or technical details
   to the user.
"""
)


# =========================================================
# CHATBOT FUNCTION
# =========================================================

def ask_chatbot(question):

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    # Get final Gemini response
    content = result["messages"][-1].content

    # Gemini can return content as a list
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


# =========================================================
# RUN CHATBOT
# =========================================================

if __name__ == "__main__":

    print("===================================")
    print("        STORE CHATBOT")
    print("===================================")
    print("Type 'exit' to stop.")
    print()

    while True:

        question = input("You: ").strip()

        if question.lower() == "exit":

            print("Chatbot stopped.")
            break

        if not question:
            continue

        try:

            answer = ask_chatbot(question)

            print()
            print("Bot:", answer)
            print()

        except Exception as e:

            print()
            print("Error:", e)
            print()