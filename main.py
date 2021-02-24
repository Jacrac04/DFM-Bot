import json
import traceback
import sys

from requests import Session
from answer_handler import AnswerHandler
import urllib3



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



class InvalidLoginDetails(Exception):
    pass


class LoginFrame():
    def __init__(self):
        print('Ensure that your google acount is NOT linked')
        email = input('Email')
        password = input('Password')
        if '@' not in email:
            email += '@utcportsmouth.org'
        try:
            Interface(email, password)
        except InvalidLoginDetails as e:
            print(e, file=sys.stderr)


class Interface:
    def __init__(self, email, password):
        self.session = Session()
        self.test_login(email, password)
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
    
    lf = LoginFrame()
