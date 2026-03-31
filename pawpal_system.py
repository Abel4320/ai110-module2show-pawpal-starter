from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    def _rank(self) -> int:
        """Return sort order integer where lower = higher priority."""
        return {"high": 1, "medium": 2, "low": 3}[self.value]


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
    pet_name: str = ""  # back-reference so skipped tasks know which pet they belong to

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def __lt__(self, other: "Task") -> bool:
        """Compare tasks by priority so sorted() returns HIGH before MEDIUM before LOW."""
        # lower rank = higher priority, so HIGH sorts first in ascending sort
        return self.priority._rank() < other.priority._rank()


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet and stamp it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return a shallow copy of all tasks for this pet."""
        return self.tasks.copy()

    def get_incomplete_tasks(self) -> list[Task]:
        """Return only tasks that have not yet been completed."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    name: str
    time_available: int  # total daily budget in minutes
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's pet list."""
        self.pets.remove(pet)

    def get_available_time(self) -> int:
        """Return the owner's total daily time budget in minutes."""
        return self.time_available


@dataclass
class DailyPlan:
    owner: Owner
    pet: Pet
    scheduled_tasks: list[Task] = field(default_factory=list)
    skipped_tasks: list[tuple[Task, str]] = field(default_factory=list)  # (task, reason)
    total_time: int = 0  # minutes consumed
    explanation: list[str] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule and accumulate its duration into total_time."""
        self.scheduled_tasks.append(task)
        self.total_time += task.duration

    def skip_task(self, task: Task, reason: str) -> None:
        """Record a skipped task with the reason it was excluded."""
        self.skipped_tasks.append((task, reason))
        self.explanation.append(f"Skipped '{task.name}': {reason}")

    def get_summary(self) -> str:
        """Return a formatted multi-line string of scheduled and skipped tasks."""
        lines = [
            f"Daily Plan — {self.pet.name} (Owner: {self.owner.name})",
            f"  Scheduled: {len(self.scheduled_tasks)} tasks, {self.total_time} min",
        ]
        for task in self.scheduled_tasks:
            lines.append(
                f"    [{task.priority.value.upper()}] {task.name} ({task.duration} min)"
            )
        if self.skipped_tasks:
            lines.append(f"  Skipped: {len(self.skipped_tasks)} tasks")
            for task, reason in self.skipped_tasks:
                lines.append(f"    - {task.name}: {reason}")
        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner and set the shared time budget."""
        self.owner = owner
        self._time_remaining: int = owner.time_available  # shared budget across all pets

    def generate_schedule(self) -> list[DailyPlan]:
        """Greedy schedule across all pets: highest-priority tasks first until time runs out."""
        return [self.generate_plan_for_pet(pet) for pet in self.owner.pets]

    def generate_plan_for_pet(self, pet: Pet) -> DailyPlan:
        """Schedule one pet's incomplete tasks against the shared time budget."""
        plan = DailyPlan(owner=self.owner, pet=pet)
        for task in self.prioritize_tasks(pet):
            if task.duration <= self._time_remaining:
                plan.add_task(task)
                self._time_remaining -= task.duration
                plan.explanation.append(
                    f"Scheduled '{task.name}' ({task.duration} min, {task.priority.value})"
                )
            else:
                plan.skip_task(
                    task,
                    f"needs {task.duration} min, only {self._time_remaining} min remaining",
                )
        return plan

    def prioritize_tasks(self, pet: Pet) -> list[Task]:
        """Return pet's incomplete tasks sorted HIGH → MEDIUM → LOW."""
        return sorted(pet.get_incomplete_tasks())

    def calculate_total_time(self, tasks: list[Task]) -> int:
        """Sum duration across a list of tasks."""
        return sum(t.duration for t in tasks)
