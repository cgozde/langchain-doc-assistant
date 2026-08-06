from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generation"))
from generate import generate_answer

app = FastAPI()

@app.get("/ask")
def ask(soru: str):
    cevap = generate_answer(soru)
    return {"cevap": cevap}