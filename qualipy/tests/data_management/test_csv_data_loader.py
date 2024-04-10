import datetime
import os
from unittest import TestCase

from qualipy.data_management.csv_data_loader import CsvDataLoader


class TestCsvDataLoader(TestCase):
    def setUp(self) -> None:
        self.csv_file_name = 'unittest_csv_dl_data.csv'
        with open(self.csv_file_name, 'w') as csv_file:
            lines = [
                '"id","first_name","last_name","active","start_date","height","activation","shift_end"\n',
                '4,"Bob","Jones","true","2019-02-05",5.5,"2019-02-05 8:00:00am","5:00:00pm"\n',
                '9,"Alice","Baker","false","2020-12-05",5.25,"2020-12-05 9:00:00pm","6:00:00pm"\n'
            ]
            csv_file.writelines(lines)
    
    def tearDown(self) -> None:
        os.remove(self.csv_file_name)

    def test_load_data(self):
        dl = CsvDataLoader()
        records = dl.load_data(data_source=self.csv_file_name)
        
        records = dl.load_data(data_source=self.csv_file_name)
        assert isinstance(records, list)
        assert isinstance(records[0], dict)
        assert len(records) == 2
        
        records = dl.load_data(data_source=self.csv_file_name, model_class='data_management.test_csv_data_loader.Employee')
        assert isinstance(records, list)
        from data_management.test_csv_data_loader import Employee
        assert isinstance(records[0], Employee)
        assert len(records) == 2

        bob = records[0]
        alice = records[1]

        assert bob.id == 4
        assert bob.first_name == 'Bob'
        assert bob.last_name == 'Jones'
        assert bob.active
        assert bob.start_date == datetime.date(year=2019, month=2, day=5)
        assert bob.height == 5.5
        assert bob.activation == datetime.datetime(year=2019, month=2, day=5, hour=8, minute=0, second=0)
        assert bob.shift_end == datetime.time(hour=17, minute=0, second=0)

        assert alice.id == 9
        assert alice.first_name == 'Alice'
        assert alice.last_name == 'Baker'
        assert not alice.active
        assert alice.start_date == datetime.date(year=2020, month=12, day=5)
        assert alice.height == 5.25
        assert alice.activation == datetime.datetime(year=2020, month=12, day=5, hour=21, minute=0, second=0)
        assert alice.shift_end == datetime.time(hour=18, minute=0, second=0)


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

