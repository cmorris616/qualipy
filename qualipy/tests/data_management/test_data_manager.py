from unittest import TestCase

import os
import datetime
from qualipy.data_management.data_loader import DataLoader

from qualipy.data_management.data_manager import DataManager
from qualipy.exceptions import DataManagerNotFoundException
from qualipy.exceptions.app_exceptions import InvalidFileExtensionException



class TestDataManager(TestCase):
    def setUp(self) -> None:
        self.csv_file_name = 'unittest_dm_data.csv'
        with open(self.csv_file_name, 'w') as csv_file:
            lines = [
                '"id","first_name","last_name","active","start_date"\n',
                '4,"Bob","Jones","true","2019-02-05"\n',
                '9,"Alice","Baker","false","2020-12-05"\n'
            ]
            csv_file.writelines(lines)
    
    def tearDown(self) -> None:
        os.remove(self.csv_file_name)

    def test_init(self):
        dm = DataManager()

        assert not dm.data_load_complete
        assert not dm.data_load_started

        assert dm.date_format == '%Y-%m-%d'
        assert dm.datetime_format == '%Y-%m-%d %I:%M:%S%p'
        assert dm.time_format == '%I:%M:%S%p'

    def test_set_get_remove_property(self):
        dm = DataManager()

        dm.set_property('test_prop', 'test_value')
        assert dm.get_property('test_prop') == 'test_value'

        dm.remove_property('test_prop')
        assert dm.get_property('test_prop') is None

        dm.remove_property('test_prop')
        assert dm.get_property('test_prop') is None

    def test_register_data_manager(self):
        with self.assertRaises(DataManagerNotFoundException):
            DataManager.get_data_manager('test_data_manager')

        dm = DataManager()

        DataManager.register_data_manager('test_data_manager', data_manager=dm)
        assert DataManager.get_data_manager('test_data_manager') == dm

    def test_register_data_loader(self):
        dm = DataManager()

        with self.assertRaises(InvalidFileExtensionException):
            dm.get_data_loader('oddfileextension')
        

        class TestDataLoader(DataLoader):
            def load_data(self, **kwargs):
                return []

        dm.register_data_loader('oddfileextension', data_loader=TestDataLoader)
        assert isinstance(dm.get_data_loader('oddfileextension'), TestDataLoader)

    def test_data_manager_loading(self):
        dm = DataManager()
        
        with self.assertRaises(FileExistsError):
            dm.load('')
        
        records = dm.load(self.csv_file_name)
        assert isinstance(records, list)
        assert isinstance(records[0], dict)
        assert len(records) == 2
        
        records = dm.load(self.csv_file_name)
        assert isinstance(records, list)
        assert isinstance(records[0], dict)
        assert len(records) == 2
        
        dm = DataManager()
        records = dm.load(self.csv_file_name, source_type='csv')
        assert isinstance(records, list)
        assert isinstance(records[0], dict)
        assert len(records) == 2
        
        dm = DataManager()
        records = dm.load(self.csv_file_name, model_class='data_management.test_data_manager.Employee')
        assert isinstance(records, list)
        from data_management.test_data_manager import Employee
        assert isinstance(records[0], Employee)
        assert len(records) == 2


class Employee:
    def __init__(self) -> None:
        self.first_name: str = ""
        self.last_name: str = ""
        self.id: int = -1
        self.active: bool = False
        self.start_date: datetime.date = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d').date()

