import datetime
import importlib
from openpyxl import load_workbook
from qualipy.data_management.data_loader import DataLoader


class ExcelDataLoader(DataLoader):
    def load_data(self, **kwargs):
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