from groq import Groq
import os
from dotenv import load_dotenv
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "retrieval"))

from search import get_relevant_chunks
load_dotenv()  # .env dosyasındaki GROQ_API_KEY'i okur

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(soru):
    get_chunks = get_relevant_chunks(soru)
    context = "\n\n".join(get_chunks)
    prompt = f"""Aşağıdaki bilgilere bakarak soruyu cevapla:

    {context}

    Soru: {soru}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

