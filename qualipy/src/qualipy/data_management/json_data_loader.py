"""
This module contains the class for loading test data from JSON files.
"""
import datetime
import importlib
import json
from qualipy.data_management.data_loader import DataLoader


class JsonDataLoader(DataLoader):
    """
    This class loads test data from JSON files.
    """
    def load_data(self, **kwargs):
        """
        Loads test data from a JSON file.  The JSON file should contain records
        keyed by the fully qualified model class with the value being a list of
        records of that model class.

        :param kwargs:
            - data_source: the path to the file containing the data

        :returns: a list of loaded records
        """
        data_source = kwargs['data_source']
        result = []

        with open(data_source, 'r') as json_file:
            data = json.load(json_file)

        for model_class_param in data.keys():
            module = importlib.import_module(model_class_param[:model_class_param.rindex('.')])
            model_class_name = model_class_param[model_class_param.rindex('.') + 1:]
            model_class = getattr(module, model_class_name)

            for record in data[model_class_param]:
                instance = model_class()

                for prop in record.keys():
                    if isinstance(getattr(instance, prop), datetime.datetime):
                        setattr(instance, prop, datetime.datetime.strptime(record[prop], self.datetime_format))
                    elif isinstance(getattr(instance, prop), datetime.date):
                        setattr(instance, prop, datetime.datetime.strptime(record[prop], self.date_format).date())
                    elif isinstance(getattr(instance, prop), datetime.time):
                        setattr(instance, prop, datetime.datetime.strptime(record[prop], self.time_format).time())
                    else:
                        setattr(instance, prop, record[prop])

                result.append(instance)

        return result