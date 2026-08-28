from groq import Groq
import os
from dotenv import load_dotenv
import sys
import time
from datetime import datetime
import json


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "retrieval"))

from prompts import PROMPTS, CURRENT_VERSION

from search import get_relevant_chunks
load_dotenv()  # .env dosyasındaki GROQ_API_KEY'i okur

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(soru):
    baslangic = time.time()

    get_chunks = get_relevant_chunks(soru)
    context = "\n\n".join(get_chunks)
    
    prompt_template = PROMPTS[CURRENT_VERSION]
    prompt = prompt_template.format(context=context, soru=soru)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
    ]
)
    cevap = response.choices[0].message.content

    print(response.usage)

    bitis = time.time()
    sure = bitis - baslangic
    

    tahmini_maliyet = (response.usage.prompt_tokens / 1_000_000 * 0.15) + (response.usage.completion_tokens / 1_000_000 * 0.60)

    log_recs = {
        "soru": soru, 
        "cevap": cevap, 
        "chunk_sayisi": len(get_chunks), 
        "sure_saniye": sure, 
        "zaman": str(datetime.now()), 
        "prompt_tokens": response.usage.prompt_tokens, 
        "completion_tokens": response.usage.completion_tokens, 
        "tahmini_maliyet_usd": tahmini_maliyet,
        "prompt_version": CURRENT_VERSION
    }

    json_string = json.dumps(log_recs)
    with open("logs.jsonl", "a") as f:
        f.write(json_string + "\n")

    return cevap


