import functools
import sys
from webbrowser import open as wbopen
import urllib.parse
from ServerStatus.server_check import CURRENT_VERSION
from tkinter import messagebox
import tkinter as tk
from tkinter import *
from datetime import datetime
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
    body = f'''**Write anything comments here**\n\n## Generated Report \n**Please do not edit**\n\nVersion : v{CURRENT_VERSION}\n\nError: {error}\n\nQuestion Details:\n'''
    if 'permid' in data.keys():
        body += f'- qnum: {data["qnum"]}\n- permid: {data["permid"]}\n- params: {data["params"]}\n'
    elif 'qid' in data.keys():
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


# Class for custom message box
# Takes in type, error message and data
# if the type is "error" then it will have two buttons, one to close window and one to open issue on github and reports the issue

class CustomMessageBox():
    def __init__(self, type, error, data):
        self.type = type
        self.error = error
        self.data = data
        self.createErrorWindow()
    
    def createErrorWindow(self):
        self.window = Toplevel()
        if self.type == 'Error':
            self.window.title("\U000026A0Error")
            # Set window icon to error
            self.window
        else:
            self.window.title("Info")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.createMessage()
        self.createButtons()
        self.createDetails()
    
    def createMessage(self):
        self.message_label = Label(self.window, text=f'An unexpected error occurred. ')
        self.message_label.grid(row=0, column=0, columnspan=2, sticky=W)
        self.message_label.grid(row=0, column=0, columnspan=2, padx=20, pady=5)
        
    def createDetails(self):
        self.details_text = Text(self.window, height = 5, width = 30)
        self.details_text.grid(row=4, column=0, columnspan=2, padx=20, pady=5)
        self.details_text.insert(tk.END, f'Unexpected Error Occurred: {self.error}')
        self.details_text.config(state=tk.DISABLED)
        self.details_text.grid_remove()
        self.details_text.state = False

    def createButtons(self):
        if self.type == 'Error':
            self.button = Button(self.window, text="Close",
                                command=lambda: self.closeWindow())
            self.button.grid(row=1, column=0, padx=10, pady=5)
            self.button = Button(self.window, text="Report Issue On GitHub",
                                command=lambda: self.reportIssue())
            self.button.grid(row=1, column=1, padx=10, pady=5)
        else:
            self.button = Button(self.window, text="Close", font=("ariel 10"),
                                command=lambda: self.closeWindow())
            self.button.grid(row=1, column=0, padx=5, pady=10)
        self.button_toggle_details = Button(self.window, text="Show Details", command=lambda: self.toggleDetails())
        self.button_toggle_details.grid(row=2, column=0, columnspan= 2, padx=5, pady=5)
    
    def toggleDetails(self):
        if self.details_text.state == False:
            # self.details_text.config(state=tk.NORMAL)
            self.details_text.grid()
            self.button_toggle_details.config(text="Hide Details")
            self.details_text.state = True
        else:
            # self.details_text.config(state=tk.DISABLED)
            self.details_text.grid_remove()
            self.button_toggle_details.config(text="Show Details")   
            self.details_text.state = False     

    def closeWindow(self):
        self.window.destroy()
    
x = CustomMessageBox("Error", "TestError", {})
