from unittest import TestCase
from unittest.mock import Mock

from qualipy.exceptions import InvalidTestingTypeError, MissingUrlError, HttpException

class TestInvalidTestingTypeError(TestCase):
    def test_message(self):
        exception = InvalidTestingTypeError('unittest')
        self.assertEqual(str(exception), '"unittest" is not a valid testing type')

class TestMissingUrlError(TestCase):
    def test_message(self):
        exception = MissingUrlError('unittest')
        self.assertEqual(str(exception), 'Missing URL')

class TestHttpException(TestCase):
    def test_message(self):
        response = Mock()
        response.status_code = 123
        response.reason = 'Running unit tests'
        response.content = 'Test response content'
        message = 'Unit Testing'
        exception = HttpException(f'{message}', response)
        self.assertEqual(str(exception), 
            f'''{message}\n
            Response Code:    {response.status_code}
            Response Reason:  {response.reason}
            Response Content: {response.content}''')