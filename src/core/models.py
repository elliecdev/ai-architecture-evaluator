from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Document:
    id: str
    content: str


@dataclass
class Constraints:
    accuracy: str      # low / medium / high
    cost_sensitivity: str
    latency_sensitivity: str
    risk_tolerance: str


@dataclass
class LLMResponse:
    answer: str
    citations: Optional[List[str]]
    cost: float
    latency_ms: int
    confidence: float
