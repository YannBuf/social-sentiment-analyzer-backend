import os
import json
import openai
from typing import Union, List, Dict, Any
from dotenv import load_dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")

async def call_openai_chat(
        prompt: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.5,
        system_prompt: str = None,
) -> Union[Dict[str, Any], str]:
    """
     Generic OpenAI GPT chat interface call function.

        Parameters:
     prompt: the content of the prompt entered by the user (which will be used as the user role).
            model: the OpenAI model to use.
            temperature: control the randomness of the generation.
            system_prompt: Optional system role definition.

        Returns:
     JSON (if successful and parsable), or raw string/error message.
     """

    messages = []
    if system_prompt:
        # request chatgpt to be expert to improve accuracy
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    #send request and got response from openai
    try:
        response = openai.chat.completions.create(
            model = model,
            messages = messages,
            temperature = temperature
        )

        result_text = response.choices[0].message.content.strip()

        #convert result into json
        try:
            return json.loads(result_text)
        except json.JSONDecodeError:
            return  result_text

    except Exception as e:
        return {"error": str(e)}
