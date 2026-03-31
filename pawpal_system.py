from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskType(Enum):
    WALK = "walk"
    FEEDING = "feeding"
    MEDICATION = "medication"
    ENRICHMENT = "enrichment"
    GROOMING = "grooming"


@dataclass
class Task:
    name: str
    duration: int  # minutes
    priority: Priority
    task_type: TaskType
    completed: bool = False


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)


@dataclass
class Owner:
    name: str
    time_available: int  # minutes
    pets: list[Pet] = field(default_factory=list)


@dataclass
class DailyPlan:
    scheduled_tasks: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)
    total_time: int = 0  # minutes
    explanation: str = ""


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet

    def generate_plan(self) -> DailyPlan:
        pass

    def prioritize_tasks(self) -> list[Task]:
        pass

    def calculate_total_time(self, tasks: list[Task]) -> int:
        pass
