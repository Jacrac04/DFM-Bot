import json
import traceback
import sys

import tkinter.messagebox as tkm

from requests import Session
from answer_handler import AnswerHandler
import urllib3

from tkinter import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def enable(childList):
    for child in childList:
        child.configure(state='normal')
def disable(childList):
    for child in childList:
        child.configure(state='disable')



class LoginFrameN(LabelFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)

        self.label_username = Label(self, text="Email")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E, pady=(10, 1), padx=(10, 1))
        self.label_password.grid(row=1, sticky=E, pady=(1, 3), padx=(10, 1))
        self.entry_username.grid(row=0, column=1, pady=(10, 1), padx=(1, 10))
        self.entry_password.grid(row=1, column=1, pady=(1, 3), padx=(1, 10))

        self.log_btn = Button(self, text="Login", command=self._login_btn_clicked)
        self.log_btn.grid(columnspan=2, pady=(1, 10), padx=(10, 10))

        #self.pack()

        # print('Ensure that your google acount is NOT linked')
        # email = input('Email')
        # password = input('Password')
    
    def _login_btn_clicked(self):
        email = self.entry_username.get()
        password = self.entry_password.get()
        if '@' not in email:
            email += '@utcportsmouth.org'
        try:
            Interface(email, password)
        except e:
            print(e, file=sys.stderr)
            tkm.showerror("Login error", "Incorrect Email or Password")


class MainFrame(LabelFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)

        self.label_url = Label(self, text="URL")
        self.label_totalQnum = Label(self, text="Num. of Qs")

        self.entry_url = Entry(self)
        self.entry_totalQnum = Entry(self)

        self.label_url.grid(row=0, sticky=E, pady=(10, 1), padx=(10, 1))
        self.label_totalQnum.grid(row=1, sticky=E, pady=(1, 3), padx=(10, 1))
        self.entry_url.grid(row=0, column=1, pady=(10, 1), padx=(1, 10))
        self.entry_totalQnum.grid(row=1, column=1, pady=(1, 3), padx=(1, 10))

        self.start_btn = Button(self, text="Start", command=self._start_btn_clicked)
        self.start_btn.grid(columnspan=2, pady=(1, 10), padx=(10, 10))

    def _start_btn_clicked(self):
        pass


class InvalidLoginDetails(Exception):
    pass


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_username = Label(self, text="Email")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.log_btn = Button(self, text="Login", command=self._login_btn_clicked)
        self.log_btn.grid(columnspan=2)

        self.pack()

        # print('Ensure that your google acount is NOT linked')
        # email = input('Email')
        # password = input('Password')
    
    def _login_btn_clicked(self):
        email = self.entry_username.get()
        password = self.entry_password.get()
        if '@' not in email:
            email += '@utcportsmouth.org'
        try:
            Interface(email, password)
        except InvalidLoginDetails as e:
            print(e, file=sys.stderr)
            tkm.showerror("Login error", "Incorrect Email or Password")

# class MainFrame(Frame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.label_username = Label(self, text="Test")
#         self.label_password = Label(self, text="Password")

#         self.entry_username = Entry(self)
#         self.entry_password = Entry(self, show="*")

#         self.label_username.grid(row=0, sticky=E)
#         self.label_password.grid(row=1, sticky=E)
#         self.entry_username.grid(row=0, column=1)
#         self.entry_password.grid(row=1, column=1)

#         self.log_btn = Button(self, text="Login", command=self._login_btn_clicked)
#         self.log_btn.grid(columnspan=2)

#         self.pack()






class Interface:
    def __init__(self, email, password):
        self.session = Session()
        self.test_login(email, password)
        root.LoginFrame.pack_forget()
        root.withdraw()
        self.handler = AnswerHandler(self.session)  
        
        self.main_loop()

    def main_loop(self):
        print('Press ctrl-c to quit')
        while True:
            url = input('\nType Question url: ')
            handler = AnswerHandler(self.session)
            res, err = handler.answer_questions_V3(url)
            if res:
                print('No more questions for this URL')
            else:
                print(f'Unexpected exception occurred: {err}', file=sys.stderr)
                traceback.print_exc()

    def test_login(self, email, password):
        login_url = 'https://www.drfrostmaths.com/process-login.php?url='
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/87.0.4280.141 Safari/537.36'}
        data = {'login-email': email, 'login-password': password}

        self.session.post(login_url, headers=headers, data=data, verify=False)
        try:
            """
            verifying user is authenticated by tests if user can load the times tables
            """
            res = self.session.get('https://www.drfrostmaths.com/homework/process-starttimestables.php', verify=False)
            json.loads(res.text)
            
            
        except BaseException:
            raise InvalidLoginDetails(f'Email: {email}, Password: {"*" * len(password)}')





if __name__ == "__main__":
    root = Tk()
    root.protocol('WM_DELETE_WINDOW', sys.exit)
    root.geometry('300x80')
    root.title('DFM Login Screen')
    lf = LoginFrame(root)
    mf = MainFrame(root)
    root.mainloop()