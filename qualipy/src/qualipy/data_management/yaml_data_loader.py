"""
This module contains the class for loading test data from YAML files.
"""
import datetime
import importlib
import time
import yaml
from qualipy.data_management.data_loader import DataLoader


class YamlDataLoader(DataLoader):
    """
    This class loads test data from YAML files.  The YAML data loader can
    handle multiple model classes. The top most keys are the fully qualified
    model class names. The subkeys are the properies. YAML can handle most
    data types. The only data type that may cause an issue is time. The time
    can be stored as a string and the time format property of the data manager
    can be used to read it.
    """
    def load_data(self, **kwargs):
        """
        Loads test data from a YAML file.

        kwargs values:
            - data_source: the path to the file containing the data
        """
        data_source = kwargs['data_source']
        result = []

        with open(data_source, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)

        for model_class_param in data.keys():
            module = importlib.import_module(model_class_param[:model_class_param.rindex('.')])
            model_class_name = model_class_param[model_class_param.rindex('.') + 1:]
            model_class = getattr(module, model_class_name)

            for record in data[model_class_param]:
                instance = model_class()

                for prop in record.keys():
                    if isinstance(getattr(instance, prop), datetime.time):
                        value = datetime.datetime.strptime(record[prop], self.time_format)
                        setattr(instance, prop,value.time())
                    else:
                        setattr(instance, prop, record[prop])

                result.append(instance)

        return result