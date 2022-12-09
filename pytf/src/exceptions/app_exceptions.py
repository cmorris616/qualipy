class InvalidTestingTypeError(Exception):
    def __init__(self, testing_type, *args):
        super().__init__(args)
        self._testing_type = testing_type

    def __str__(self):
        return f'"{self._testing_type}" is not a valid testing type'

class MissingUrlError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self):
        return 'Missing URL'