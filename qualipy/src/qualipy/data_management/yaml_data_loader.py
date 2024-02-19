import datetime
import importlib
import time
import yaml
from qualipy.data_management.data_loader import DataLoader


class YamlDataLoader(DataLoader):
    def load_data(self, **kwargs):
        """
        Loads test data from a JSON file.  The JSON file should contain records
        keyed by the fully qualified model class with the value being a list of
        records of that model class.  For example:

        models.model1.Model1:
            - prop1: value1
              prop2: value2
            - prop1: value3
              prop2: value4
        models.another_model.AnotherModel:
            - prop3: value5
              prop4: value6

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