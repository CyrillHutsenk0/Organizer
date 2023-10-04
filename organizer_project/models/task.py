from dataclasses import dataclass


@dataclass
class Task:
    description = None
    id_ = None

    def __init__(self, description: str):
        from organizer_project.config import TASK_LIST

        task_id_step = 1
        task_id = 0
        if TASK_LIST:
            task_id = TASK_LIST[-1].id_ + task_id_step

        self.id_ = task_id
        self.description = description
