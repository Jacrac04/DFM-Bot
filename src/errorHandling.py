import functools
import sys

# Define Errors
class NoQuestionFound(Exception):
    pass

class ParseError(Exception):
    pass

class InvalidURLException(BaseException):
    def __init__(self, url, *args):
        self.__url = url
        super().__init__(*args)

    def __str__(self):
        return f"Invalid URL {self.__url}"

class TestError(BaseException):
    pass


# Define Wraps
def questionCatchWrap(func):
    @functools.wraps(func)
    def stub(self, *args, **kwargs):
        try:
            return func(self, *args, *kwargs)
        except NoQuestionFound:  # raised in parser, questions finished
            return True, True
        except KeyboardInterrupt:
            sys.exit()  # quits script
        except BaseException as e:
            print(str(e), self.currentData)
    return stub

def mainWrap(func):
    @functools.wraps(func)
    def stub(self, *args, **kwargs):
        try:
            return func(self, *args, *kwargs)
        except KeyboardInterrupt:
            sys.exit()  # quits script
        except BaseException as e:
            print(str(e))
    return stub