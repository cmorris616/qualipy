"""
This module contains the base class for data loaders.
"""
import abc


class DataLoader:
    """
    This is the base class for data loaders.
    """
    def __init__(self):
        """
        Initializes the datetime-related formats for this data loader
        """
        self.date_format = '%Y-%m-%d'
        self.datetime_format = '%Y-%m-%d %I:%M:%S%p'
        self.time_format = '%I:%M:%S%p'

    @abc.abstractmethod
    def load_data(self, **kwargs):
        """
        Loads the data from the data source
        """
        pass

    @staticmethod
    def resolve_bool(value):
        """
        Resolves strings to boolean values.  All string comparisons
        are case-insensitive.

        True values:
            * true
            * 1
            * on
            * yes

        False values:
            * false
            * 0
            * off
            * no
        """
        if value is None:
            return False
        
        if isinstance(value, str):
            if value.lower() in ['true', '1', 'on', 'yes']:
                return True
            elif value.lower() in ['false', '0', 'off', 'no']:
                return False
            else:
                raise ValueError(f"Invalid boolean value '{value}'")
            
        if isinstance(value, int):
            if value == 0:
                return False
            if value== 1:
                return True
            else:
                raise ValueError(f"Invalid boolean value '{value}'")