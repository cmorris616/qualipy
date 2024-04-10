import datetime
import json
import os
from unittest import TestCase

from qualipy.data_management.json_data_loader import JsonDataLoader


class TestJsonDataLoader(TestCase):
    def setUp(self) -> None:
        self.json_file_name = 'unittest_json_dl_data.json'
        
        test_data = {
            "data_management.test_json_data_loader.Employee": [
                {
                    "id": 4,
                    "first_name": "Bob",
                    "last_name": "Jones",
                    "active": True,
                    "start_date": "02/05/2019",
                    "height": 5.5
                },
                {
                    "id": 9,
                    "first_name": "Alice",
                    "last_name": "Baker",
                    "active": False,
                    "start_date": "12/05/2020",
                    "height": 5.25
                }
            ],
            "data_management.test_json_data_loader.Task": [
                {
                    "id": 3,
                    "description": "Add more data loaders",
                    "due_date": "10/30/2024",
                    "completion_datetime": "04/20/2024 03:56",
                    "start_date": "01/15/2024",
                    "start_time": "13:20"
                }
            ]
        }

        with open(self.json_file_name, 'w') as test_file:
            json.dump(test_data, indent=2, fp=test_file)

    def tearDown(self) -> None:
        os.remove(self.json_file_name)

    def test_load_data(self):
        dl = JsonDataLoader()
        dl.date_format = '%m/%d/%Y'
        dl.datetime_format = '%m/%d/%Y %H:%M'
        dl.time_format = '%H:%M'
        
        records = dl.load_data(data_source=self.json_file_name)
        assert isinstance(records, list)
        from data_management.test_json_data_loader import Employee, Task
        assert len(records) == 3
        assert isinstance(records[0], Employee)
        assert isinstance(records[1], Employee)
        assert isinstance(records[2], Task)

        bob = records[0]
        alice = records[1]
        task = records[2]

        assert bob.id == 4
        assert bob.first_name == 'Bob'
        assert bob.last_name == 'Jones'
        assert bob.active
        assert bob.start_date == datetime.date(year=2019, month=2, day=5)
        assert bob.height == 5.5

        assert alice.id == 9
        assert alice.first_name == 'Alice'
        assert alice.last_name == 'Baker'
        assert not alice.active
        assert alice.start_date == datetime.date(year=2020, month=12, day=5)
        assert alice.height == 5.25

        assert task.id == 3
        assert task.description == 'Add more data loaders'
        assert task.due_date == datetime.date(year=2024, month=10, day=30)
        assert task.completion_datetime == datetime.datetime(year=2024, month=4, day=20, hour=3, minute=56)
        assert task.start_date == datetime.date(year=2024, month=1, day=15)
        assert task.start_time == datetime.time(hour=13, minute=20, second=0)

class Employee:
    def __init__(self) -> None:
        self.first_name: str = ""
        self.last_name: str = ""
        self.id: int = -1
        self.active: bool = False
        self.start_date: datetime.date = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d').date()
        self.height: float = 0.0
        self.activation: datetime.datetime = datetime.datetime.strptime('1970-01-01 8:00:00', '%Y-%m-%d %I:%M:%S')
        self.shift_end: datetime.time = datetime.datetime.strptime('1970-01-01 8:00:00', '%Y-%m-%d %I:%M:%S').time()


class Task:
    def __init__(self) -> None:
        self.id: int = -1
        self.description: str = ""
        self.due_date: datetime.date = datetime.date.max
        self.completion_datetime: datetime.datetime = datetime.datetime.max
        self.start_time: datetime.time = datetime.time.max
        self.start_date: datetime.date = datetime.date.max