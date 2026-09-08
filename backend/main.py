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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(order_router)


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(request: ChatRequest):
    answer = ask_chatbot(request.question)
    return {"answer": answer}


@app.get("/")
def home():
    return {"message": "Store Chatbot API is running"}