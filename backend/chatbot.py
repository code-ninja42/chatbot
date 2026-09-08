import requests
import os

from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

API_BASE_URL = "https://chatbot-project-pro5.onrender.com"


@tool
def get_products():
    """Get all products from the store."""
    response = requests.get(
        f"{API_BASE_URL}/products",
        timeout=30
    )
    response.raise_for_status()
    return response.json()


@tool
def get_orders():
    """Get all orders from the store."""
    response = requests.get(
        f"{API_BASE_URL}/orders",
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def ask_chatbot(question):

    q = question.lower().strip()

    # Greeting
    if q in ["hi", "hii", "hello", "hey", "hello!"]:
        return "Hello! 👋 How can I help you with our store?"


    # Get products directly
    if any(word in q for word in [
        "product",
        "price",
        "stock",
        "available",
        "availability",
        "cheapest",
        "lowest price",
        "highest price",
        "most expensive"
    ]):

        data = get_products.invoke({})

        products = data.get("products", [])

        if not products:
            return "No products found."


        # Highest price
        if (
            "highest price" in q
            or "most expensive" in q
            or "maximum price" in q
        ):
            product = max(
                products,
                key=lambda x: float(x["price"])
            )

            return (
                f"The product with the highest price is "
                f"{product['name']} at ₹{product['price']}."
            )


        # Lowest price
        if (
            "lowest price" in q
            or "lowest" in q
            or "cheapest" in q
            or "minimum price" in q
        ):
            product = min(
                products,
                key=lambda x: float(x["price"])
            )

            return (
                f"The product with the lowest price is "
                f"{product['name']} at ₹{product['price']}."
            )


        # Highest stock
        if "highest stock" in q:
            product = max(
                products,
                key=lambda x: int(x["stock"])
            )

            return (
                f"{product['name']} has the highest stock "
                f"with {product['stock']} units."
            )


        # Lowest stock
        if "lowest stock" in q:
            product = min(
                products,
                key=lambda x: int(x["stock"])
            )

            return (
                f"{product['name']} has the lowest stock "
                f"with {product['stock']} units."
            )


        # Product list
        result = "Here are our products:\n\n"

        for product in products:
            result += (
                f"• {product['name']} - "
                f"₹{product['price']} "
                f"(Stock: {product['stock']})\n"
            )

        return result


    # Orders
    if "order" in q or "tracking" in q:

        data = get_orders.invoke({})

        orders = data.get("orders", [])

        if not orders:
            return "No orders found."

        result = "Here are the orders:\n\n"

        for order in orders:
            result += (
                f"• Order #{order['id']} - "
                f"{order['customer_name']} - "
                f"{order['status']}\n"
            )

        return result


    return (
        "I can help you with products, prices, "
        "stock, availability, and orders."
    )