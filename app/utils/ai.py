import os
from pydantic import BaseModel
import json
from typing import Dict, List, Any

import openai

from dotenv import load_dotenv


def _get_openai_key() -> str:
    return os.environ["OPENAI_API_KEY"]


load_dotenv(".env")
openai.api_key = _get_openai_key()


class TextSummary(BaseModel):
    source_text: str
    summary: str
    model: str
    usage: Dict[str, Any]
    finish_reason: str


class ChainOfDensityPrompt:
    template = """
    Article: {{ ARTICLE }}

    You will generate increasingly concise, entity-dense summaries of the above Article.

    Repeat the following 2 steps 5 times.

    Step 1. Identify 1-3 informative Entities ("; " delimited) from the Article which are missing from the previously generated summary.
    Step 2. Write a new, denser summary of identical length which covers every entity and detail from the previous summary plus the Missing Entities.

    A Missing Entity is:
    - Relevant: to the main story.
    - Specific: descriptive yet concise (5 words or fewer).
    - Novel: not in the previous summary.
    - Faithful: present in the Article.
    - Anywhere: located anywhere in the Article.

    Guidelines:
    - The first summary should be long (4-5 sentences, ~80 words) yet highly non-specific, containing little information beyond the entities marked as missing. Use overly verbose language and fillers (e.g., "this article discusses") to reach ~80 words.
    - Make every word count: rewrite the previous summary to improve flow and make space for additional entities.
    - Make space with fusion, compression, and removal of uninformative phrases like "the article discusses".
    - The summaries should become highly dense and concise yet self-contained, e.g., easily understood without the Article.
    - Missing entities can appear anywhere in the new summary.
    - Never drop entities from the previous summary. If space cannot be made, add fewer new entities.

    Remember, use the exact same number of words for each summary.

    Answer in JSON. The JSON should be a list (length 5) of dictionaries whose keys are "Missing_Entities" and "Denser_Summary".
    """

    def __init__(self) -> None:
        pass

    def format(self, article: str) -> str:
        return self.template.replace("{{ ARTICLE }}", article)


class Summarizer:
    def __init__(self, model: str) -> None:
        self._prompt = ChainOfDensityPrompt()
        self._model = model
    
    def summarize(
        self, 
        text: str
    ) -> TextSummary:
        input = self._prompt.format(text)
        response = openai.ChatCompletion.create(
            model=self._model,
            temperature=0.01,
            messages=[
                {"role": "user", "content": input}
            ]
        )

        try:
            density_chain: List[Dict[str, str]] = json.loads(response.choices[0].message.content)

            # should be list but can be dict with single entry.
            if isinstance(density_chain, dict):
                density_chain = [density_chain]
            
            summary = density_chain[-1]["Denser_Summary"]
            
        except Exception as exc:
            raise Exception(f"Could not parse response from OpenAI: {response}") from exc
        
        text_summary = TextSummary(
            source_text=input,
            summary=summary,
            finish_reason=response.choices[0].finish_reason,
            model=self._model,
            usage=dict(response.usage)
        )

        return text_summary

