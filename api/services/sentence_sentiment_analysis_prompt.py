# services/analyzer.py

from typing import Union, Dict, Any
from api.services.openai_client import call_openai_chat  # 你提供的通用调用函数

# 你之前的情感分析完整英文 prompt 模板
ANALYSIS_PROMPT_TEMPLATE = """
You are an advanced English sentiment analysis AI.

Please analyze the following English text with these instructions:

1. Determine the overall sentiment: "positive", "negative", or "neutral".

2. Provide a confidence score for this overall sentiment, expressed as a percentage from 0% to 100%.
   - For example, if the sentiment is "negative", the confidence indicates how strongly negative it is.

3. Based on the overall sentiment detected, break down the emotions into relevant categories with scores between 0 and 1 (0 means absence, 1 means very strong presence):

   - If the overall sentiment is "positive", provide scores for these emotions: joy, trust, anticipation, surprise.
   - If the overall sentiment is "negative", provide scores for these emotions: anger, sadness, fear, disgust.
   - If the overall sentiment is "neutral", provide scores for these emotions: calmness, acceptance, boredom, neutrality.

   Only include the emotion categories relevant to the overall sentiment in your response.

4. Extract up to 5 key keywords or key phrases that best summarize the content.

Please return the result strictly in the following JSON format:

{{
  "sentiment": "positive / negative / neutral",
  "confidence": 0,            // percentage number, e.g. 87 means 87%
  "emotions": {{
    // only the relevant categories as explained above, each score 0.0 - 1.0
  }},
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}

Here is the text to analyze:

\"\"\"
{input_text}
\"\"\"
"""

async def analyze_english_text(input_text: str) -> Union[Dict[str, Any], str]:
    prompt = ANALYSIS_PROMPT_TEMPLATE.format(input_text=input_text)
    system_prompt = "You are a helpful and accurate English sentiment analysis assistant."
    result = await call_openai_chat(prompt=prompt, system_prompt=system_prompt, temperature=0.4)
    return result
