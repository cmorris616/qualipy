import datetime
from qualipy.data_management.data_loader import DataLoader
from models.employee import Employee
from models.task import Task

class CustomDataLoader(DataLoader):
    def load_data(self, **kwargs):
        bob = Employee()
        alice = Employee()
        task = Task()

        bob.id = 4
        bob.first_name = 'Bob'
        bob.last_name = 'Jones'
        bob.active = True
        bob.start_date = datetime.date(year=2019, month=2, day=5)

        alice.id = 9
        alice.first_name = 'Alice'
        alice.last_name = 'Baker'
        alice.active = False
        alice.start_date = datetime.date(year=2020, month=12, day=5)

        task.id = 3
        task.description = "Add more data loaders"
        task.due_date = datetime.date(year=2024, month=10, day=30)
        task.completion_datetime = datetime.datetime(year=2024, month=4, day=20, hour=3, minute=56)
        task.start_date = datetime.date(year=2024, month=1, day=15)
        task.start_time = datetime.time(hour=13, minute=20)

        result = [bob, alice, task]
        return result