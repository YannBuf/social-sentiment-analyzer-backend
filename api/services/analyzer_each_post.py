# services/analyzer.py

import openai
import json
from typing import List
from db.models.data_unit import AnalyzableItem


def format_posts_for_batch_prompt(items: List[AnalyzableItem]) -> str:
    lines = []
    for idx, item in enumerate(items, start=1):
        block = f"""Post {idx}:
Title: {item.title}
Content: {item.content}
Comments: {" | ".join(item.comments)}"""
        lines.append(block)
    return "\n\n".join(lines)


async def analyze_items_batch(items: List[AnalyzableItem]) -> dict:
    formatted_posts = format_posts_for_batch_prompt(items)

    batch_prompt = f"""
You are a social media analyst. Please analyze the following Reddit posts. For each post, return:

- sentiment: positive / negative / neutral
- summary: one-sentence summary
- keywords: 3-5 keywords

Input:
{formatted_posts}

Return as a JSON array like this:

[
  {{
    "id": 1,
    "sentiment": "positive",
    "summary": "Post discusses AI advancements",
    "keywords": ["AI", "technology", "OpenAI"]
  }},
  ...
]
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": batch_prompt}],
            temperature=0.5,
        )
        result_json = json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        return {"error": str(e)}

    # 聚合情绪与关键词
    sentiment_count = {"positive": 0, "neutral": 0, "negative": 0}
    all_keywords = []

    for r in result_json:
        s = r.get("sentiment", "neutral")
        if s in sentiment_count:
            sentiment_count[s] += 1
        all_keywords.extend(r.get("keywords", []))

    # 总体总结（单独再问 GPT 一次）
    overall = await get_overall_summary(items)

    return {
        "aggregate": {
            "sentiment_distribution": sentiment_count,
            "top_keywords": all_keywords,
            "summary": overall.get("summary", ""),
            "overall_sentiment": overall.get("sentiment", "neutral"),
            "overall_keywords": overall.get("keywords", [])
        },
        "per_item_results": result_json
    }


async def get_overall_summary(items: List[AnalyzableItem]) -> dict:
    combined_text = "\n\n".join(
        f"Title: {item.title}\nContent: {item.content}" for item in items
    )

    summary_prompt = f"""
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
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.5,
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        return {
            "sentiment": "unknown",
            "summary": f"Summary generation failed: {e}",
            "keywords": []
        }
