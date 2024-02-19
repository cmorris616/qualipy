import datetime

class Task:
    def __init__(self) -> None:
        self.id: int = -1
        self.description: str = ""
        self.due_date: datetime.date = datetime.date.max
        self.completion_datetime: datetime.datetime = datetime.datetime.max
        self.start_time: datetime.time = datetime.time.max
        self.start_date: datetime.date = datetime.date.max