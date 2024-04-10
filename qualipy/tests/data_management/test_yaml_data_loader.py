import datetime
import os
from unittest import TestCase

import yaml

from qualipy.data_management.yaml_data_loader import YamlDataLoader


class TestYamlDataLoader(TestCase):
    def setUp(self) -> None:
        self.yaml_file_name = 'unittest_yaml_dl_data.yaml'

        with open(self.yaml_file_name, 'w') as yaml_file:
            yaml.dump(stream=yaml_file, data={
                'data_management.test_yaml_data_loader.Employee': [
                    {
                        'id': 4,
                        'first_name': 'Bob',
                        'last_name': 'Jones',
                        'active': True,
                        'start_date': datetime.date(year=2019, month=2, day=5)
                    },
                    {
                        'id': 9,
                        'first_name': 'Alice',
                        'last_name': 'Baker',
                        'active': False,
                        'start_date': datetime.date(year=2020, month=12, day=5)
                    }
                ],
                'data_management.test_yaml_data_loader.Task': [
                    {
                        'id': 3,
                        'description': 'Add more data loaders',
                        'due_date': datetime.date(year=2024, month=10, day=30),
                        'completion_datetime': datetime.datetime(year=2024, month=4, day=20, hour=3, minute=56, second=0),
                        'start_date': datetime.date(year=2024, month=1, day=15),
                        'start_time': datetime.time(hour=13, minute=20, second=0).strftime('%I:%M:%S%p')
                    }
                ]
            })

    def tearDown(self) -> None:
        os.remove(self.yaml_file_name)

    def test_data_load(self):
        dl = YamlDataLoader()
        
        records = dl.load_data(data_source=self.yaml_file_name)
        assert isinstance(records, list)
        from data_management.test_yaml_data_loader import Employee, Task
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

        assert alice.id == 9
        assert alice.first_name == 'Alice'
        assert alice.last_name == 'Baker'
        assert not alice.active
        assert alice.start_date == datetime.date(year=2020, month=12, day=5)

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