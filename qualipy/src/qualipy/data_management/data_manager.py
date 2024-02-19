from os import path
from time import sleep

from qualipy.data_management.csv_data_loader import CsvDataLoader
from qualipy.data_management.excel_data_loader import ExcelDataLoader
from qualipy.data_management.json_data_loader import JsonDataLoader
from qualipy.data_management.xml_data_loader import XmlDataLoader
from qualipy.exceptions.app_exceptions import InvalidFileExtensionException
from qualipy.data_management.yaml_data_loader import YamlDataLoader
from qualipy.exceptions import DataManagerNotFoundException
from qualipy.data_management.data_loader import DataLoader


class DataManager:

    _DATE_FORMAT_KEY = 'date_format'
    _DATETIME_FORMAT_KEY = 'datetime_format'
    _TIME_FORMAT_KEY = 'time_format'

    _data_managers = {}

    def __init__(self):
        self._data_load_started = False
        self._data_load_complete = False
        self.date_format = '%Y-%m-%d'
        self.datetime_format = '%Y-%m-%d %I:%M:%S%p'
        self.time_format = '%I:%M:%S%p'
        self._properties = {}
        self._records = []

        self._data_loaders = {
            'csv': CsvDataLoader,
            'xlsx': ExcelDataLoader,
            'json': JsonDataLoader,
            'xml': XmlDataLoader,
            'yml': YamlDataLoader,
            'yaml': YamlDataLoader
        }

    @property
    def data_load_started(self):
        return self._data_load_started
    
    @property
    def data_load_complete(self):
        return self._data_load_complete
    
    def set_property(self, property_name: str, property_value):
        self._properties[property_name] = property_value

    def get_property(self, property_name):
        if property_name not in self._properties.keys():
            return None
        
        return self._properties[property_name]
    
    def remove_property(self, property_name):
        if property_name not in self._properties.keys():
            return
        
        del self._properties[property_name]

    def load(self, data_source, source_type=None, **kwargs):
        """
            Loads the data from the specified data source.  A data loader is used
            based on the source type.  If the source type is not provided, the file
            extension (.csv, .xml, .xlsx, .json) of the data source is used to
            determine the appropriate data loader to use.

            :param str data_source: the source for the data
            :param str source_type: the type for the source.  Valid values are
                                    xml, xlsx, csv, json, or any other registered type.
                                    If the source_type is ommitted or is None, the file
                                    extension of the data_source will be used to determine
                                    the source type.
        """
        if self.data_load_complete:
            return self._records
        
        while self.data_load_started and not self.data_load_complete:
            sleep(2)

        self._data_load_started = True

        try:
            kwargs['data_source'] = data_source

            if not path.exists(data_source):
                raise FileExistsError(f"'{path.abspath(data_source)}' does not exist")
            
            if source_type is None:
                file_ext = path.splitext(data_source)[1].replace('.', '')
            else:
                file_ext = source_type
            
            data_loader = self.get_data_loader(file_extension=file_ext)

            self.set_formats(data_loader)
            
            results = data_loader.load_data(**kwargs)
            self._data_load_complete = True
            self._data_load_started = False

        finally:
            self._data_load_started = False

        self._records = results

        return self._records
    
    def set_formats(self, data_loader: DataLoader):
        data_loader.date_format = self.date_format
        data_loader.time_format = self.time_format
        data_loader.datetime_format = self.datetime_format
    
    def get_data_loader(self, file_extension):
        file_extension = file_extension.lower()

        if file_extension not in self._data_loaders.keys():
            raise InvalidFileExtensionException(f'{file_extension} is not supported')
        
        return self._data_loaders[file_extension]()
    
    def register_data_loader(self, file_extension, data_loader):
        self._data_loaders[file_extension] = data_loader
    
    @classmethod
    def get_data_manager(cls, data_manager_name):
        if data_manager_name not in cls._data_managers.keys():
            raise DataManagerNotFoundException(
                f'The data manager {data_manager_name} has not been registered.')
        return cls._data_managers[data_manager_name]
    
    @classmethod
    def register_data_manager(cls, name, data_manager):
        cls._data_managers[name] = data_manager
