"""
This module contains the class for loading CSV data.
"""
from qualipy.data_management.data_loader import DataLoader
import csv
import importlib
import datetime

class CsvDataLoader(DataLoader):
    """
    Handles reading test data from CSV files.  Note that CSV files can use
    different delimiters other than commas.
    """
    def load_data(self, **kwargs):
        """
        Loads the data from the specified CSV file.
        A header row is required.  The column headers must match the properties of
        the model class to be returned.
        
        :param kwargs:
            * data_source: the csv file to read.
            
            * delimiter: the delimiter to use when reading the file.

            * model_class: the fully qualified name of the model class represented by the data being read.
              If this is ommitted, a list of dictionary objects will be returned with the first row
              of the file being treated as the keys.

            * quoting: the type of quoting used in the file.  csv.QUOTE_NONNUMERIC is the default and
              recommended value.  Using other quoting may affect data types as the data is read.
              The quoting can be a subset of the constants from the csv package:

              * csv.QUOTE_NONNUMERIC
                Instructs writer objects to quote all non-numeric fields.
        
                Instructs reader objects to convert all non-quoted fields to type float.
        
              * csv.QUOTE_NONE
                Instructs writer objects to never quote fields. When the current delimiter
                occurs in output data it is preceded by the current escapechar character.
                If escapechar is not set, the writer will raise Error if any characters that
                require escaping are encountered.
            
                Instructs reader objects to perform no special processing of quote characters.
        
              * csv.QUOTE_NOTNULL
                Instructs writer objects to quote all fields which are not None. This is
                similar to QUOTE_ALL, except that if a field value is None an empty (unquoted)
                string is written.
            
                Instructs reader objects to interpret an empty (unquoted) field as None and to
                otherwise behave as QUOTE_ALL.
            
                New in version 3.12.
        
              * csv.QUOTE_STRINGS
                Instructs writer objects to always place quotes around fields which are strings.
                This is similar to QUOTE_NONNUMERIC, except that if a field value is None an
                empty (unquoted) string is written.
            
                Instructs reader objects to interpret an empty (unquoted) string as None and to otherwise behave as QUOTE_NONNUMERIC.
            
                New in version 3.12.

        :returns: a list of loaded records
        """
        data_source = kwargs['data_source']
        delimiter = kwargs.get('delimiter', ',')
        model_class_param = kwargs.get('model_class', None)
        quoting = kwargs.get('quoting', csv.QUOTE_NONNUMERIC)

        records = []
        model_class = None

        if model_class_param is not None:
            module = importlib.import_module(model_class_param[:model_class_param.rindex('.')])
            model_class_name = model_class_param[model_class_param.rindex('.') + 1:]
            model_class = getattr(module, model_class_name)

        with open(data_source) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter, quoting=quoting)

            header_row = None

            for row in csv_reader:
                if header_row is None:
                    header_row = row
                    continue

                rec_dict = {}
                rec = None

                if model_class is not None:
                    rec = model_class()

                for i in range(0, len(header_row)):
                    col_name = header_row[i]

                    if model_class is None:
                        rec_dict[header_row[i]] = row[i]
                    else:
                        if isinstance(getattr(rec, col_name), bool):
                            setattr(rec, col_name, DataLoader.resolve_bool(row[i]))
                        elif isinstance(row[i], float):
                            if float(row[i]) == int(row[i]):
                                setattr(rec, col_name, int(row[i]))
                            else:
                                setattr(rec, col_name, float(row[i]))
                        elif isinstance(getattr(rec, col_name), datetime.datetime):
                            setattr(rec, col_name, datetime.datetime.strptime(row[i], self.datetime_format))
                        elif isinstance(getattr(rec, col_name), datetime.date):
                            setattr(rec, col_name, datetime.datetime.strptime(row[i], self.date_format).date())
                        elif isinstance(getattr(rec, col_name), datetime.time):
                            setattr(rec, col_name, datetime.datetime.strptime(row[i], self.time_format).time())
                        else:
                            setattr(rec, col_name, row[i])

                if model_class is None:
                    records.append(rec_dict)
                else:
                    records.append(rec)

        return records