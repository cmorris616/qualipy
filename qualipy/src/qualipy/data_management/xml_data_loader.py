"""
This module contains the class for loading test data from XML files.
"""
import datetime
import importlib
import xml.etree.ElementTree as ET
from qualipy.data_management.data_loader import DataLoader


class XmlDataLoader(DataLoader):
    """
    This class loads test data from XML files.  The data types will be matched
    based on the data type of the associated property in the model class.

    The XML data loader can handle multiple model classes. The XML must have a
    root node. The node can be anything (i.e. data). The tags immediately under
    the root node should be the fully qualified model class names. Child elements
    of the model class nodes will be the property names with values as desired.
    The formats for date, time, and datetime are used when loading the data.
    """
    def load_data(self, **kwargs):
        """
        Loads the data from the specified data source.

        :param kwargs:
            * data_source: the path to the XML file containing the test data.
        """
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