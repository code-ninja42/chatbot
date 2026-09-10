import os
import requests

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain.agents import create_agent


load_dotenv()


API_BASE_URL = "https://chatbot-project-pro5.onrender.com"


# -------------------------------------------------
# PRODUCT TOOL
# -------------------------------------------------

@tool
def get_products():
    """
    Get all products from the store.

    Use this tool for product names, prices, stock,
    availability, categories, cheapest products,
    most expensive products and product comparisons.
    """

    response = requests.get(
        f"{API_BASE_URL}/products",
        timeout=30
    )

    response.raise_for_status()

    return response.text


# -------------------------------------------------
# ORDER TOOL
# -------------------------------------------------

@tool
def get_orders():
    """
    Get all orders from the store.

    Use this tool for order information, order ID,
    customer name, order status, delivery status,
    tracking number, quantity and total.
    """

    response = requests.get(
        f"{API_BASE_URL}/orders",
        timeout=30
    )

    response.raise_for_status()

    return response.text


# -------------------------------------------------
# GROQ LLM
# -------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


# -------------------------------------------------
# LANGCHAIN AGENT
# -------------------------------------------------

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


IMPORTANT TOOL RULES:

1. For ANY question about products, ALWAYS use get_products.

2. For ANY question about price, ALWAYS use get_products.

3. For ANY question about stock, ALWAYS use get_products.

4. For ANY question about availability, ALWAYS use get_products.

5. For cheapest or most expensive products, ALWAYS use get_products.

6. For ANY question about orders, ALWAYS use get_orders.

7. For order status, ALWAYS use get_orders.

8. For delivery status, ALWAYS use get_orders.

9. For tracking information, ALWAYS use get_orders.

10. If the user provides an order ID, find that order
    in the get_orders result.

11. If the customer name and order ID are provided,
    verify both using get_orders.

12. NEVER invent product information.

13. NEVER invent order information.

14. NEVER guess prices, stock, availability,
    order status, delivery status or tracking numbers.

15. Only use actual information returned by the
    store tools.


OUTSIDE QUESTIONS:

You ONLY have information about this store.

If the question is unrelated to the store, say:

"Sorry, I can only help with information related to this store."


Do not answer general knowledge, coding questions,
personal advice, news, entertainment or unrelated questions.


GREETINGS:

Simple greetings such as hello, hi and hey are allowed.

Do not call store tools for simple greetings.


ANSWER STYLE:

- Clear
- Concise
- Natural
- Helpful

Do not show technical details.

Do not mention tools.

Do not mention LangChain.

Do not mention Gemini.

Do not mention Groq.

Use actual store data.
"""
)


# -------------------------------------------------
# CHAT FUNCTION
# -------------------------------------------------

def ask_chatbot(question):

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

        content = response["messages"][-1].content


        # Normal text response
        if isinstance(content, str):
            return content


        # Structured response
        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, dict):

                    if "text" in item:
                        text_parts.append(
                            str(item["text"])
                        )

                else:
                    text_parts.append(
                        str(item)
                    )

            return " ".join(text_parts).strip()


        # Other response types
        return str(content)


    except Exception as e:

        print("CHATBOT ERROR:", e)

        error_message = str(e)

        # Groq rate limit / quota
        if (
            "429" in error_message
            or "rate_limit" in error_message.lower()
            or "quota" in error_message.lower()
        ):
            return (
                "Sorry, the AI service limit has been "
                "reached. Please try again later."
            )

        # Service unavailable
        if (
            "503" in error_message
            or "service unavailable" in error_message.lower()
        ):
            return (
                "Sorry, the AI service is temporarily "
                "unavailable. Please try again later."
            )

        # Other errors
        return (
            "Sorry, I could not process your request "
            "right now."
        )