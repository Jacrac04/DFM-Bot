import json
import traceback
import sys

from requests import Session
from answer_handler import AnswerHandler
from generateTask import taskGenerator
import urllib3
from random import uniform

from tkinter import *
import tkinter.messagebox as tkm
from tkinter.messagebox import askyesno

import sys


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self,text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    def write(self,text):
        self.text_area.configure(state='normal')
        self.text_area.insert(END, text)
        self.text_area.see("end")
        self.text_area.configure(state='disabled')
    def flush(self): # needed for file like object
        pass


class InvalidLoginDetails(Exception):
    pass


class UserInterface(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "Dr Frost Bot")

        container = Frame(self)

        self.lf = LoginFrame(self, container)
        self.lf.grid(column=0, row=1, padx=10, pady=10)
        self.mf = MainFrame(self, container)
        self.mf.grid(column=0, row=2, padx=10, pady=10)

        self.of = OutputFrame(self, container)
        self.of.grid(column=1, row=1, rowspan=2, padx=10, pady=10)
        
        self.gf = SubWindowManagerFrame(self)
        self.gf.grid(column=0, row=3, columnspan=2, padx=10, pady=10)



        self.nf = NotesFrame(self, container)
        self.nf.grid(column=0, row=4, columnspan=2, padx=10, pady=(1,10))

        self.disable(self.mf.winfo_children())
        self.disable(self.gf.winfo_children())

        self.interface = Interface()

    def enable(self, childList):
        for child in childList:
            try:
                child.configure(state='normal')
            except:
                pass
    def enablegrandchild(self, childList):
        for child in childList:
            try:
                child.configure(state='normal')
            except:
                try:
                    grandchildList = child.winfo_children()
                    for grandchild in grandchildList:
                        grandchild.configure(state='normal')
                except:
                    pass

    def disable(self, childList):
        for child in childList:
            try:
                child.configure(state='disable')
            except:
                try:
                    grandchildList = child.winfo_children()
                    for grandchild in grandchildList:
                        grandchild.configure(state='disable')
                except:
                    try:
                        greatgrandchildList = grandchild.winfo_children()
                        for greatgrandchild in greatgrandchildList:
                            greatgrandchild.configure(state='disable')
                    except:
                        greatgreatgrandchildList = greatgrandchild.winfo_children()
                        for greatgreatgrandchild in greatgreatgrandchildList:
                            greatgreatgrandchild.configure(state='disable')


class SubWindowManagerFrame(LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.label_subWin = Label(self, text="Advanced Functions:")
        self.label_subWin.grid(column=0, row=1, padx=10, pady=10)

        self.btn_taskGen = Button(self, text="Task Generator", command=self.openTaskGenerator)
        self.btn_taskGen.grid(column=1, row=1, padx=10, pady=10)

    def openTaskGenerator(self):
        self.taskGeneratorWindow= Toplevel(self.master)
        self.gf = TaskGeneratorFrame(self.taskGeneratorWindow, self.master)
        self.gf.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
        self.btn_taskGenClose = Button(self.taskGeneratorWindow, text="Close", command=self.taskGeneratorWindow.destroy)
        self.btn_taskGenClose.grid(column=0, row=2, columnspan=2, padx=10, pady=10)



class LoginFrame(LabelFrame):
    def __init__(self, master, cont):
        super().__init__(master)

        self.master = master

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

    
    def _login_btn_clicked(self):
        email = self.entry_username.get()
        password = self.entry_password.get()
        if '@' not in email:
            email += '@utcportsmouth.org'
        try:
            self.master.interface.test_login(email, password)
            self.master.enable(self.master.mf.winfo_children())
            self.master.enablegrandchild(self.master.gf.winfo_children())
        except InvalidLoginDetails as e:
            print(e, file=sys.stderr)
            tkm.showerror("Login error", "Incorrect Email or Password")


class MainFrame(LabelFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.frame_totalQnum = Frame (self)

        self.label_url = Label(self, text="URL/AAID")
        self.entry_url = Entry(self)

        self.label_url.grid(row=0, sticky=E, pady=(10, 1), padx=(10, 1))
        self.entry_url.grid(row=0, column=1, pady=(10, 1), padx=(1, 10))
        
        self.autoSubmit = BooleanVar()
        self.autoSubBtn = Radiobutton(self, 
               text="Auto Submit:",
               variable=self.autoSubmit, 
               value=True,
                command=lambda:self.master.enable(self.frame_totalQnum.winfo_children()))
        self.autoSubBtn.grid(row=1, columnspan=2, sticky=W, pady=(10, 0), padx=(10, 10))


        self.label_totalQnum = Label(self.frame_totalQnum, text="Num. of Qs to Answer")
        self.entry_totalQnum = Entry(self.frame_totalQnum)

        self.label_totalQnum.grid(row=2, column=1, columnspan=1, sticky=W, pady=(0, 1), padx=(1, 10))
        self.entry_totalQnum.grid(row=3, column=1, columnspan=1, pady=(1, 0), padx=(1, 10))

        self.label_minDelay = Label(self.frame_totalQnum, text="Min Delay (seconds(ish)):")
        self.entry_minDelay = Entry(self.frame_totalQnum)
        self.label_maxDelay = Label(self.frame_totalQnum, text="Max Delay (seconds(ish)):")
        self.entry_maxDelay = Entry(self.frame_totalQnum)

        self.label_minDelay.grid(row=4, column=1, columnspan=1, sticky=W, pady=(0, 1), padx=(1, 10))
        self.entry_minDelay.grid(row=5, column=1, columnspan=1, pady=(1, 0), padx=(1, 10))
        self.label_maxDelay.grid(row=6, column=1, columnspan=1, sticky=W, pady=(0, 1), padx=(1, 10))
        self.entry_maxDelay.grid(row=7, column=1, columnspan=1, pady=(1, 0), padx=(1, 10))


        self.frame_totalQnum.grid(row=3, columnspan=2, pady=(1, 0))


        self.manSubBtn = Radiobutton(self, 
                    text="Manual Submit",
                    variable=self.autoSubmit,               
                    value=False,
                    command=lambda: self.master.disable(self.frame_totalQnum.winfo_children()))
        self.manSubBtn.grid(row=4, columnspan=2, sticky=W, pady=(5, 10), padx=(10, 10))

        
        self.start_btn = Button(self, text="Start", command=self._start_btn_clicked)
        self.start_btn.grid(columnspan=2, pady=(1, 10), padx=(10, 10))

    @staticmethod
    def checkDelay(min, max):
        if min < 3:
            answer = askyesno(title='Confirmation',
                message='By having a short delay you could get banned, This has only been tested with delays greater than 5. \nDo you want to continue?')
            if not answer: 
                    return False
        if min==max:
                answer = askyesno(title='Confirmation',
                message='By having the same min and max there is no varriance, you COULD BE banned. \nDo you want to continue?')
                if not answer: 
                    return False
        return True
    
    def checkQnum(self, qnum):
        qnum = int(qnum)
        if not self.shownBefore:
            if qnum > 5: # Prob here
                answer = askyesno(title='Warning',
                    message=f'You can get banned for over 300 questions completed but the warning appears at 100. Current qnum: {qnum}\nDo you want to continue?')
                if not answer: 
                        return False
                self.shownBefore = True
        if qnum > 7:
            answer = askyesno(title='Critical Warning',
                message=f'You WILL BE banned for over 300 questions completed. Current qnum: {qnum}\nDo you want to continue?')
            if not answer: 
                    return False
        print('here')
        return True

    def _start_btn_clicked(self, ):
        self.url = None
        self.totalQnum = 0
        self.minDelay = 0
        url = self.entry_url.get()
        try:
            if self.autoSubmit.get():
                self.totalQnum = self.entry_totalQnum.get()
                self.totalQnum = int(self.totalQnum)
                self.minDelay = self.entry_minDelay.get()
                self.minDelay = float(self.minDelay)
                self.maxDelay = self.entry_maxDelay.get()
                self.maxDelay = float(self.maxDelay)
                confResp = self.checkDelay(self.minDelay, self.maxDelay)
                if not confResp:
                    raise TypeError
            if len(url) == 8:
                self.url = 'https://www.drfrostmaths.com/do-question.php?aaid=' + url
            else:
                self.url = url
            self.shownBefore = False
            self.master.interface.main_loop(self.url, self.totalQnum, self.minDelay, self.maxDelay, self.autoSubmit.get(), self.master, self)
        except TypeError or ValueError:
            tkm.showerror("Input error", "Invalid totalQnum or Delay")
        

class TaskGeneratorFrame(LabelFrame):
    def __init__(self, master, masterMaster):
        super().__init__(master)

        #self.masterMaster = masterMaster
         
        self.frame_mode = LabelFrame(self)
        self.frame_questionNum = Frame (self.frame_mode)

        self.mode = BooleanVar()
        self.mode1Btn = Radiobutton(self.frame_mode, 
                text="Set Amount of Qs to generate:",
                variable=self.mode,               
                value=1,
                command=lambda: self.master.master.enable(self.frame_questionNum.winfo_children()))
        self.mode1Btn.grid(row=1, column=0, columnspan=1, sticky=W, pady=(5, 1), padx=(10, 10))

        self.questionNum = StringVar(self.frame_mode)
        choices = ['4','6','8','10','12','15','20','25','30','35']
        self.questionNum.set(choices[0])
        self.label_questionNum = Label(self.frame_questionNum, text="Num. of Qs:")
        self.menu_questionNum = OptionMenu(self.frame_questionNum, self.questionNum, *choices)

        self.label_questionNum.grid(row=2, column=1, columnspan=1, sticky=W, pady=(0, 1), padx=(1, 10))
        self.menu_questionNum.grid(row=2, column=2, columnspan=1, pady=(1, 0), padx=(1, 10))

        self.mode0Btn = Radiobutton(self.frame_mode, 
               text="Infinite          ",
               variable=self.mode, 
               value=0,
                command=lambda: self.master.master.disable(self.frame_questionNum.winfo_children()))
        self.mode0Btn.grid(row=3, column=0, columnspan=1, sticky=W, pady=(0, 10), padx=(10, 10))

        self.frame_questionNum.grid(row=2, columnspan=2, pady=(1, 0))
        #self.master.disable(self.frame_mode.winfo_children())

        self.frame_mode.grid(row=1, column=1, rowspan=2, columnspan=1, pady=(10, 10), padx=(20, 10))

        self.frame_interleave = LabelFrame(self)

        self.intlerleave = BooleanVar()
        self.intlerleave0Btn = Radiobutton(self.frame_interleave, 
               text="Don't Interleave Qs Types",
               variable=self.intlerleave, 
               value=0)
        self.intlerleave0Btn.grid(row=1, column=2, columnspan=1, sticky=W, pady=(10, 2), padx=(10, 10))
        self.intlerleave1Btn = Radiobutton(self.frame_interleave, 
               text="Interleave Qs Types",
               variable=self.intlerleave, 
               value=1)
        self.intlerleave1Btn.grid(row=2, column=2, columnspan=1, sticky=W, pady=(2, 10), padx=(10, 10))

        self.frame_interleave.grid(row=1, column=2, columnspan=1, pady=(10, 0), padx=(10, 10))


        self.frame_amount = LabelFrame(self)
        self.label_amount = Label(self.frame_amount, text="Num. of Skills:")
        self.entry_amount = Entry(self.frame_amount, width=12)

        self.label_amount.grid(row=2, column=1, columnspan=1, sticky=W, pady=(0, 1), padx=(1, 10))
        self.entry_amount.grid(row=2, column=2, columnspan=1, pady=(1, 0), padx=(1, 10))
        self.frame_amount.grid(row=2, column=2, columnspan=1, pady=(0, 10), padx=(10, 10))

        self.frame_tid = LabelFrame(self)

        self.label_tid = Label(self.frame_tid, text='Include Questions That Are:')
        self.label_tid.grid(row=0, column=0)

        self.doUnseen = BooleanVar()
        self.doStarted = BooleanVar()
        self.doComplete = BooleanVar()

        self.doUnseen.set(False)
        self.doStarted.set(False)
        self.doComplete.set(False)

        self.doUnseenBtn = Checkbutton(self.frame_tid, text='Unseen',variable=self.doUnseen, onvalue=True, offvalue=False)
        self.doUnseenBtn.grid(row=1, column=0)
        self.doStartedBtn = Checkbutton(self.frame_tid, text='Started',variable=self.doStarted, onvalue=True, offvalue=False)
        self.doStartedBtn.grid(row=2, column=0)
        self.doCompleteBtn = Checkbutton(self.frame_tid, text='Completed',variable=self.doComplete, onvalue=True, offvalue=False)
        self.doCompleteBtn.grid(row=3, column=0)

        self.frame_tid.grid(row=1, column=3, columnspan=1, rowspan=2, pady=(10, 10), padx=(10, 20))


        self.start_btn = Button(self, text="Generate", command=self._Generate_btn_clicked)
        self.start_btn.grid(column= 1, columnspan=3, pady=(1, 10), padx=(10, 10))


    def _Generate_btn_clicked(self):
        tidNum = []
        if self.doUnseen.get():
            tidNum.append(0)
        if self.doStarted.get():
            tidNum.append(1)
        if self.doComplete.get():
            tidNum.append(2)
        try:
            amountSkills = self.entry_amount.get()
            amountSkills = int(amountSkills)
        except TypeError or ValueError:
            tkm.showerror("Input error", "Invalid Amount - Num of Skills ≈654 max")        
        try:
            self.master.master.interface.generate_task(self.mode.get(), self.intlerleave.get(), tidNum, amountSkills, int(self.questionNum.get()), self.master)
        except TypeError or ValueError:
            tkm.showerror("Input error", "")




class OutputFrame(LabelFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.textbox = Text(self, height=22, width=50)
        self.textbox.configure(state='disabled')
        self.textbox.grid(row=0, column=0)

        scrollb = Scrollbar(self, command=self.textbox.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.textbox['yscrollcommand'] = scrollb.set

    def write(self, text):
        self.textbox.insert(END, text) 

    def flush(self): # needed for file like object
        pass

class NotesFrame(LabelFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        #self.geometry('40x40')
        self.label = Label(self, text="This is a Dr Frost Bot made by github.com/@Jacrac04")
        self.label.grid(row=0, column=0, padx=(98, 20), pady=5)
        self.btn_help = Button(self, text="Instructions And Help", command= lambda: HelpWindow(master))
        self.btn_help.grid(row=0, column=1, padx=(20, 98), pady=5)

class HelpFrame(LabelFrame):
    def __init__(self, master, controller):
        super().__init__(master)

class HelpWindow(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Instructions")

        self.textbox = Text(self, height=15, width=125, borderwidth=0, font=("Helvetica", 10))
        self.textbox.insert(1.0, "Instructions:\n  For Better insructions visit https://github.com/Jacrac04/DFM-Bot\n  1) Firstly login\n  2) Enter the question url:\n       - This should look like https://www.drfrostmaths.com/do-question.php?aaid=12345678\n       - Make sure that there is nothing else like qnum=5 in it.\n   3) Select manual or auto submit.\n       - Auto submit lets you enter the amount of the questions for it to answer and it will go through and answer them for you.\n       - Manual submit will give you the answer for the currrent question and then you can enter it, then repeat this process. \nAbout:\n  This is a Bot for drfrostmaths.com. It was made by github.com/Jacrac04.\n   If you found this usefull please star this on https://github.com/Jacrac04/DFM-Bot. It really helps, thanks.\n   You can find the latest version at https://github.com/Jacrac04/DFM-Bot/releases\n   If this gets any questions wrong feel free to open an issue and report it here: https://github.com/Jacrac04/DFM-Bot/issues/new/choose")
        self.textbox.configure(state="disabled", inactiveselectbackground=self.textbox.cget("selectbackground"))
        self.textbox.grid(row=0, column=0)


        self.btn_quit = Button(self, text="Close", command=self.destroy)
        self.btn_quit.grid(column=0)


       



class Login():
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
    def __init__(self):
        self.session = Session()


    #This despritly needs rewriting.
    def main_loop(self, url=None, totalQnum=0, minDelay=0, maxDelay=0, autoSubmit = True, root=None, subMain=None):
        handler = AnswerHandler(self.session)
        #Legacy
        if url==None:
            print('Press ctrl-c to quit')
            while True:
                url = input('\nType Question url: ')
                res, err = handler.answer_questions_V3(url, autoSubmit)
                if res:
                    print('No more questions for this URL')
                else:
                    print(f'Unexpected exception occurred: {err}', file=sys.stderr)
                    traceback.print_exc()
        else:
            if totalQnum > 0:
                for q in range(1,totalQnum+1): #from 1 to toalt +1 as its q=1 when question_num =1
                    answer, qnum = handler.answer_question_V4_part1(url)
                    checkRes = subMain.checkQnum(qnum)
                    if not checkRes:
                        break
                    if answer:
                        pass
                    else:
                        print(f'Unexpected exception occurred: {err}', file=sys.stderr)
                        traceback.print_exc()
                        break
                    print(f'Answer:{answer}\nNow waiting')

                    root.update()
                    delay = int(uniform(minDelay, maxDelay))
                    for time in range(0,delay*100,1):
                        root.after(10, root.update())
                    print('Answered\n')
                    res, err = handler.answer_question_V4_part2()
                    
                print('Done')

            else:
                answer, qnum = handler.answer_question_V4_part1(url)
                print(f'Question {qnum}: {answer}')
                if answer:
                    pass
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
    
    def generate_task(self, modeNum, interleave, tidNum, amountSkills, amountQuestions, root=None):
        generator = taskGenerator(self.session)
        res, err = generator.makeTask_V1(modeNum, interleave, tidNum, amountSkills, amountQuestions)
        if res:
            print(f'Generated URL: {res}\n')
        if err:
            print(err)






if __name__ == "__main__":
    app = UserInterface()
    sys.stdout = StdoutRedirector(app.of.textbox)
    app.mainloop()
