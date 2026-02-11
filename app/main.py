# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import rag_chain

app = FastAPI(title="Dental Coverage Assistant")

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    return {
        "answer": rag_chain.invoke(q.question)
    }
