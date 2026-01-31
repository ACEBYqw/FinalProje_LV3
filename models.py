from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class UserProfile:
    user_id: int
    interests: List[str]
    skills: List[str]
    education_level: str
    wants_remote: bool
    risk_tolerance: int
    language: str = "tr"
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class CareerLevel:
    title: str
    min_experience: int
    description: str

@dataclass
class CareerPath:
    name: str
    interests: List[str]
    skills: List[str]
    education_level: str
    remote_possible: bool
    risk_level: int
    levels: List[CareerLevel]
    tags: List[str] = field(default_factory=list)
