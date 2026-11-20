from copy import deepcopy
from itertools import count

USERS: dict[int, dict] = {
    1: {"id": 1, "name": "Anna Nowak", "email": "anna.nowak@example.com"},
    2: {"id": 2, "name": "Jan Kowalski", "email": "jan.kowalski@example.com"},
    3: {"id": 3, "name": "Ewa Wiśniewska", "email": "ewa.wisniewska@example.com"},
}

PROJECTS: dict[int, dict] = {
    1: {"id": 1, "name": "TaskBoard", "description": "Aplikacja rozwijana na laboratoriach"},
    2: {"id": 2, "name": "Praca dyplomowa", "description": None},
}

TASKS: dict[int, dict] = {
    1: {"id": 1, "project_id": 1, "title": "Przygotować środowisko", "status": "done", "priority": "high", "assignee_id": 1},
    2: {"id": 2, "project_id": 1, "title": "Przeczytać RFC 9110", "status": "in_progress", "priority": "medium", "assignee_id": 2},
    3: {"id": 3, "project_id": 1, "title": "Zaprojektować API", "status": "open", "priority": "low", "assignee_id": None},
    4: {"id": 4, "project_id": 2, "title": "Wybrać temat", "status": "open", "priority": "high", "assignee_id": 3},
}

class Storage:
    def __init__(self) -> None:
        self.users = deepcopy(USERS)
        self.projects = deepcopy(PROJECTS)
        self.tasks = deepcopy(TASKS)
        self.next_project_id = count(3)
        self.next_task_id = count(5)

storage = Storage()

def get_storage() -> Storage:
    return storage
