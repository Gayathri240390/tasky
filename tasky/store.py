import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


class TaskStore:
    """Persists tasks as JSON in a single file."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.tasks: list[Task] = []
        if self.path.exists():
            self.tasks = [Task(**t) for t in json.loads(self.path.read_text("utf-8"))]

    def save(self) -> None:
        self.path.write_text(json.dumps([asdict(t) for t in self.tasks], indent=2), "utf-8")

    def add(self, title: str) -> Task:
        next_id = max((t.id for t in self.tasks), default=0) + 1
        task = Task(next_id, title)
        self.tasks.append(task)
        return task

    def get(self, task_id: int) -> Task:
        for t in self.tasks:
            if t.id == task_id:
                return t
        raise KeyError(f"no task with id {task_id}")

    def complete(self, task_id: int) -> Task:
        task = self.get(task_id)
        task.done = True
        return task

    def remove(self, task_id: int) -> Task:
        task = self.get(task_id)
        self.tasks.remove(task)
        return task
