import abc


class DataLoader:
    def __init__(self):
        self.date_format = '%Y-%m-%d'
        self.datetime_format = '%Y-%m-%d %I:%M:%S%p'
        self.time_format = '%I:%M:%S%p'

    @abc.abstractmethod
    def load_data(self, **kwargs):
        pass

    @staticmethod
    def resolve_bool(value):
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