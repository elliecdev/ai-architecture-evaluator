from abc import ABC, abstractmethod
from typing import List
from .models import Document, Constraints, LLMResponse


class LLMArchitecture(ABC):

    @abstractmethod
    def run(
        self,
        question: str,
        documents: List[Document],
        constraints: Constraints
    ) -> LLMResponse:
        pass
