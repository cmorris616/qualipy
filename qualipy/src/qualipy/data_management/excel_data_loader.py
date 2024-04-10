"""
This module contains the class that handles loading test data from
Excel files.
"""
import datetime
import importlib
from openpyxl import load_workbook
from qualipy.data_management.data_loader import DataLoader


class ExcelDataLoader(DataLoader):
    """
    This class handles loading data from Excel files.  The data must be contained
    in a worksheet whose name is the fully qualified class name of the model class
    that represents the data being loaded.  The Excel file can contain multiple
    worksheets as long as the worksheets are named with the fully qualified model
    class name.
    """
    def load_data(self, **kwargs):
        """
        Loads the data from the Excel file.  The data type for the data being
        read must be set in the Excel file.  For example, if a particular field
        contains a datetime value, then the cell must be formatted as a datetime
        field.  Values not formatted correctly may be read as a string.

        In the event that a data type is not available in Excel, the associated
        property for the model class will be checked in order to attempt to match
        the data type.

        :param kwargs:
            * data_source: the path to the Excel file containing the test data
        """
        data_source = kwargs['data_source']

        workbook = load_workbook(data_source)

        result = []

        for worksheet in workbook.worksheets:
            module = importlib.import_module(worksheet.title[:worksheet.title.rindex('.')])
            model_class_name = worksheet.title[worksheet.title.rindex('.') + 1:]
            model_class = getattr(module, model_class_name)

            header_row = []

            for row in worksheet.rows:
                if len(header_row) == 0:
                    for cell in row:
                        header_row.append(cell.value)
                    continue

                instance = model_class()

                for cell in row:
                    prop = header_row[cell.col_idx - 1]
                    value = cell.value
                    if isinstance(getattr(instance, prop), bool):
                        setattr(instance, prop, DataLoader.resolve_bool(value))
                    elif isinstance(getattr(instance, prop), float):
                        setattr(instance, prop, float(value))
                    elif isinstance(getattr(instance, prop), int):
                        setattr(instance, prop, int(value))
                    elif isinstance(getattr(instance, prop), datetime.datetime):
                        setattr(instance, prop, value)
                    elif isinstance(getattr(instance, prop), datetime.date):
                        setattr(instance, prop, value.date())
                    elif isinstance(getattr(instance, prop), datetime.time):
                        setattr(instance, prop, value)
                    else:
                        setattr(instance, prop, value)

                result.append(instance)
        
        return result