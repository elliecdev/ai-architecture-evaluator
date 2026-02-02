import os
import time
import requests
from typing import List

from src.core.interfaces import LLMArchitecture
from src.core.models import Document, Constraints, LLMResponse
from src.core.metrics import estimate_confidence


HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")


class PromptOnlyArchitecture(LLMArchitecture):
    """
    Prompt-only LLM architecture.
    Uses a single model call with no external grounding.
    """

    def run(
        self,
        question: str,
        documents: List[Document],
        constraints: Constraints
    ) -> LLMResponse:

        prompt = self._build_prompt(question, constraints)

        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}"
        }

        payload = {
            "inputs": prompt
        }

        start_time = time.time()
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        latency_ms = int((time.time() - start_time) * 1000)

        response.raise_for_status()
        result = response.json()

        # Hugging Face text-generation responses vary slightly by model
        answer_text = result[0]["generated_text"]

        estimated_cost = self._estimate_cost(prompt, answer_text)

        return LLMResponse(
            answer=answer_text,
            citations=None,
            cost=estimated_cost,
            latency_ms=latency_ms,
            confidence=estimate_confidence(answer_text),
        )

    def _build_prompt(self, question: str, constraints: Constraints) -> str:
        return (
            "Answer the following question clearly and concisely.\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )

    def _estimate_cost(self, prompt: str, answer: str) -> float:
        """
        Hugging Face free tier does not expose token usage.
        This is a rough placeholder for comparative purposes.
        """
        token_estimate = (len(prompt) + len(answer)) / 4
        return round(token_estimate * 0.000001, 6)
