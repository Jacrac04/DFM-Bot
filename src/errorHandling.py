import functools
import sys
from webbrowser import open as wbopen
import urllib.parse

VERSION = 'v5.0.0'
# A way to create Issues on github
# https://github.com/Jacrac04/DFM-Bot/issues/new?assignees=&labels=Bug%2FIssue&template=bug-or-issue-report.md&title=&body=Hello
# assignees = list of people to assign to
# labels = list of labels to add to issue
# template = template to use
# title = title of issue
# body = body of issue

# Ideal Template
    ## User Comments
    # **Write anything comments here**
    # ## Generated Report 
    # **Please do not edit**
    # Version : v5.0.0
    # Error: Unsupported Data Type
    # Question Details:
    # - qnum: '1'
    # - permid: 770
    # - params: '["y", 5, 1, 50, 10, 2, 14]'

def createBodyFromError(error, data):
    body = f'''**Write anything comments here**\n\n## Generated Report \n**Please do not edit**\n\nVersion : v{VERSION}\n\nError: {error}\n\nQuestion Details:\n'''
    if data['permid']:
        body += f'- qnum: {data["qnum"]}\n- permid: {data["permid"]}\n- params: {data["params"]}\n'
    elif data['qid']:
        body += f'- qnum: {data["qnum"]}\n- quid: {data["quid"]}\n'
    return body
# urllib.parse.quote(createBodyFromError('TestError',))


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
            wbopen(f'https://github.com/Jacrac04/DFM-Bot/issues/new?body={urllib.parse.quote(createBodyFromError("TestError",self.currentData))}')
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



# wbopen(f'https://github.com/Jacrac04/DFM-Bot/issues/new?{urllib.parse.quote(createBodyFromError('TestError',))}')
