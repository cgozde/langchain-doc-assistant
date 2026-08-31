from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generation"))
from generate import generate_answer

app = FastAPI()

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    with open("src/api/static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/ask")
def ask(soru: str):
    cevap = generate_answer(soru)
    return {"cevap": cevap}