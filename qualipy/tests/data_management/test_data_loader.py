import os
from unittest import TestCase
from qualipy.data_management.data_loader import DataLoader
from qualipy.data_management.data_manager import DataManager


class TestDataLoader(TestCase):
    def setUp(self) -> None:
        self.csv_file_name = 'unittest_dl_data.csv'
        with open(self.csv_file_name, 'w') as csv_file:
            lines = [
                '"id","first_name","last_name","active","start_date"\n',
                '4,"Bob","Jones","true","2019-02-05"\n',
                '9,"Alice","Baker","false","2020-12-05"\n'
            ]
            csv_file.writelines(lines)
    
    def tearDown(self) -> None:
        os.remove(self.csv_file_name)

    def test_data_loader(self):
        class TestDataLoader(DataLoader):
            def load_data(self, **kwargs):
                super().load_data(**kwargs)
                return []
            
        dm = DataManager()
        dm.register_data_loader('csv', TestDataLoader)
        records = dm.load(data_source=self.csv_file_name)
        assert len(records) == 0

        with self.assertRaises(ValueError):
            DataLoader.resolve_bool('bad value')

        assert DataLoader.resolve_bool('tRue')
        assert DataLoader.resolve_bool('1')
        assert DataLoader.resolve_bool('yEs')
        assert DataLoader.resolve_bool('ON')
        assert not DataLoader.resolve_bool('faLse')
        assert not DataLoader.resolve_bool('0')
        assert not DataLoader.resolve_bool('nO')
        assert not DataLoader.resolve_bool('OFF')
        assert not DataLoader.resolve_bool(0)
        assert not DataLoader.resolve_bool(None)
        assert DataLoader.resolve_bool(1)

        with self.assertRaises(ValueError):
            DataLoader.resolve_bool(3)