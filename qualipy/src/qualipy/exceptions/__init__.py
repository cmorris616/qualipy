"""
This modules contains the exceptions for the library.
"""

class DataManagerNotFoundException(Exception):
    """
    Indicates that the requested data manager was not found.
    """
    pass

class InvalidTestingTypeError(Exception):
    """
    Indicates that the specified testing type is invalid.  The valid testing
    type are regression and progression.
    """
    def __init__(self, testing_type, *args):
        """
        Initializes an instance of this exception with the specified testing type.
        """
        super().__init__(args)
        self._testing_type = testing_type

    def __str__(self):
        return f'"{self._testing_type}" is not a valid testing type'

class MissingUrlError(Exception):
    """
    Indicates that a URL is missing.
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self):
        return 'Missing URL'

class HttpException(Exception):
    """
    Raised when an HTTP exception occurs.  The message includes the
    response code, reason, and content.
    """
    def __init__(self, msg, response, *args):
        self._message = \
            f'''{msg}\n
            Response Code:    {response.status_code}
            Response Reason:  {response.reason}
            Response Content: {response.content}'''
        super().__init__(args)
    
    def __str__(self):
        return self._message

class InvalidFileExtensionException(Exception):
    """
    Indicates that an invalid file extension was used.
    """
    pass