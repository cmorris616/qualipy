import datetime
import importlib
import xml.etree.ElementTree as ET
from qualipy.data_management.data_loader import DataLoader


class XmlDataLoader(DataLoader):
    def load_data(self, **kwargs):
        data_source = kwargs['data_source']
        tree = ET.parse(data_source)
        root = tree.getroot()

        result = []

        for record in root:
            module = importlib.import_module(record.tag[:record.tag.rindex('.')])
            model_class_name = record.tag[record.tag.rindex('.') + 1:]
            model_class = getattr(module, model_class_name)
            
            instance = model_class()

            for prop in record:
                if isinstance(getattr(instance, prop.tag), bool):
                    setattr(instance, prop.tag, DataLoader.resolve_bool(prop.text))
                elif isinstance(getattr(instance, prop.tag), float):
                    setattr(instance, prop.tag, float(prop.text))
                elif isinstance(getattr(instance, prop.tag), int):
                    setattr(instance, prop.tag, int(prop.text))
                elif isinstance(getattr(instance, prop.tag), datetime.datetime):
                    setattr(instance, prop.tag, datetime.datetime.strptime(prop.text, self.datetime_format))
                elif isinstance(getattr(instance, prop.tag), datetime.date):
                    setattr(instance, prop.tag, datetime.datetime.strptime(prop.text, self.date_format).date())
                elif isinstance(getattr(instance, prop.tag), datetime.time):
                    setattr(instance, prop.tag, datetime.datetime.strptime(prop.text, self.time_format).time())
                else:
                    setattr(instance, prop.tag, prop.text)

            result.append(instance)

        return result