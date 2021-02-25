import json
import traceback
import sys

import tkinter.messagebox as tkm

from requests import Session
from answer_handler import AnswerHandler
import urllib3

from tkinter import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



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


class Interface:
    def __init__(self, email, password):
        self.session = Session()
        self.test_login(email, password)
        root.destroy()
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
    root.mainloop()