from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

class ContentType(Enum):
    COURSE = "cours"
    EXERCISE_BASIC = "exercices_entrainement"
    EXERCISE_ADVANCED = "exercices_approfondissement"
    EXERCISE_CHALLENGE = "exercices_defis"
    EVALUATION_FORMATIVE = "evaluation_formative"
    EVALUATION_SUMMATIVE = "evaluation_sommative"
    CORRECTION = "corrections"

@dataclass
class Chapter:
    number: int
    title: str
    objectives: List[str]
    prerequisites: List[str]
    duration_hours: int
    key_concepts: List[str]
    competencies: List[str]

@dataclass
class APIConfig:
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4000
    temperature: float = 0.3
    use_cache: bool = True
    batch_processing: bool = True
    retry_attempts: int = 3

@dataclass
class CourseConfig:
    level: str
    sessions_per_year: int
    curriculum_sources: List[Dict[str, str]]
    resources: List[Dict[str, str]]
    output_path: str = "./output"

@dataclass
class PedagogicalProgram:
    level: str
    total_sessions: int
    chapters: List[Chapter]
    general_objectives: List[str]
    evaluation_criteria: Dict[str, Any] 