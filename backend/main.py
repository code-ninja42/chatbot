from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from products import router as product_router
from order import router as order_router
from chatbot import ask_chatbot


app = FastAPI(
    title="Store Chatbot API",
    version="1.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Product APIs
app.include_router(product_router)

# Order APIs
app.include_router(order_router)


# Chat request
class ChatRequest(BaseModel):
    question: str


# Chatbot API
@app.post("/chat")
def chat(request: ChatRequest):
    answer = ask_chatbot(request.question)

    return {
        "answer": answer
    }


# Home API
@app.get("/")
def home():
    return {
        "message": "Store Chatbot API is running"
    }