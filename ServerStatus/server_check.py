#This cheack Github for updates or warnings
import tkinter.messagebox as tkm
import requests

def check_status(CURRENT_VERSION):
    resp = requests.get('https://raw.githubusercontent.com/Jacrac04/DFM-Bot/develop/ServerStatus/status.txt')
    version, status, msg = resp.text.split(', ')
    if version != CURRENT_VERSION:
        tkm.showwarning("Warning",f'There is a new version, {version}. The current version is {CURRENT_VERSION}. Updating is recommened as it can cause you to get banned from DFM if you dont. Updates availbile from github.com/Jacrac04/DFM-Bot/releases')
    if status == 'Normal':
        if msg != 'None':
            tkm.showinfo("Information", msg)
        return False, (False, False)
    elif status == 'Error':
        if msg != 'None':
            tkm.showerror("Error", msg)
        tkm.showerror("Unknown Error", "It is not recogmended to use this until this is resolved.")
    else:
        tkm.showerror("Unknown Status", "It is not recogmended to use this until this is resolved.")



