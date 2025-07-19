# backend/services/analyzer.py

import openai
import os
import json
from typing import List
from db.models.data_unit import AnalyzableItem
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def analyze_items(items: List[AnalyzableItem]) -> dict:
    texts = []
    for item in items:
        text = f"{item.title}\n{item.content}"
        if item.comments:
            text += "\n评论：" + " | ".join(item.comments)
        texts.append(text)

    combined_text = "\n\n---\n\n".join(texts)

    prompt = f"""
You are a social media analyst. Please analyze the overall sentiment and topics in the following social media content:

{combined_text}

Return the result in the following JSON format:

{{
  "sentiment": "positive / negative / neutral",
  "summary": "brief summary of the public opinion",
  "keywords": ["keyword1", "keyword2", "..."]
}}
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        result_text = response.choices[0].message.content.strip()
        return json.loads(result_text)
    except Exception as e:
        return {"error": str(e)}
