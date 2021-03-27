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

    def makeTask_V1(self, modeNum=0, interleave=0, tidNum=[0]):
        if modeNum == 0:
            mode = 'nostop'
        else:
            return None, 'Mode not impemented'
        keySkillsIDsList = []
        for num in tidNum:
            if num == 0:
                tid = 'unseen'
            elif num == 1:
                tid = 'started'
            elif num == 2:
                tid = 'complete'
            keySkillsIDs, err = self.getSkillID(tid)
            if err:
                return None, 'Error Generating Questions'
            keySkillsIDsList.extend(keySkillsIDs)
        
        fullURL = self.get_task_url_base + f'permid={str(keySkillsIDsList)[1:-1]}&interleave={interleave}&cmode={mode}'
        res = self.sesh.get(fullURL, allow_redirects=True)
        return res.url, False



    def getSkillID(self, tid='unseen'):
        res = self.sesh.post(self.get_unseen_url_base + tid)
        resData = json.loads(res.text)
        keySkillsIDs = []
        for x in resData['keyskilllist']:
            keySkillsIDs.append(x['permid'])
        if len(keySkillsIDs):
            return keySkillsIDs, False
        else:
            return None, True



