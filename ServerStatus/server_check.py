#This check Github for updates or warnings
import requests

CURRENT_VERSION = 'v5.0.0'

def check_status():
    resp = requests.get('https://raw.githubusercontent.com/Jacrac04/DFM-Bot/master/ServerStatus/status.txt')
    version, status, msg = resp.text.split(', ')
    return version, status, msg




