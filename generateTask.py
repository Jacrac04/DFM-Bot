import functools
import json
import sys
from statistics import mean

class taskGenerator:
    def __init__(self, session):
        self.sesh = session
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                ' Chrome/87.0.4280.141 Safari/537.36'}
        self.get_unseen_url_base = 'https://www.drfrostmaths.com/util-gettopickeyskills.php?tid='
        self.get_task_url_base = 'https://www.drfrostmaths.com/process-startkeyskillassessment.php?'
        self.permid_blacklist = []

    def makeTask_V1(self, modeNum=0, interleave=0, tidNum):
        if tidNum == 0:
            tid = 'unseen'
        elif tidNum == 1:
            tid = 'started'
        elif tidNum == 2:
            tid = 'complete'
        if modeNum == 0:
            mode = 'nostop'
        else:
            print('Mode not impemented')
        

        keySkillsIDs, err = self.getSkillID(tid)
        if err:
            print('Error Generating Questions')
        
        fullURL = self.get_task_url_base + f'permid{str(todo)[1:-1]}&interleave={interleave}&cmode={mode}''
        res = self.sesh.get(url2, allow_redirects=True)
        print(f'Generated URL: {res.url}')


        #interleave=1&cmode=nostop&permid

    def getSkillID(self, tid='unseen'):
        res = self.sesh.post(get_unseen_url_base + tid)
        resData = json.loads(res.text)
        keySkillsIDs = []
        for x in resData['keyskilllist']:
            keySkillsIDs.append(x['permid'])
        if len(keySkillsIDs):
            return keySkillsIDs, False
        else:
            return None, True



