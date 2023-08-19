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

class HttpException(Exception):
    def __init__(self, msg, response, *args):
        self._message = \
            f'''{msg}\n
            Response Code:    {response.status_code}
            Response Reason:  {response.reason}
            Response Content: {response.content}'''
        super().__init__(args)
    
    def __str__(self):
        return self._message
