import re
from json import JSONDecoder
import json

from bs4 import BeautifulSoup


class NoQuestionFound(Exception):
    pass


class ParseError(Exception):
    pass


QNUM_REGEX = re.compile(r"var qnum = .+;")
FIND_DIGIT_REGEX = re.compile(r"\d+")
AAID_REGEX = re.compile(r"aaid=.+")


class Parser:
    @staticmethod
    def parse_V2(page: str):
        try:
            #Upgrade so it allows for changes to the question page
            current_question_script = str(Parser.find_tags(page)[-2])
            _json = list(Parser.extract_json(current_question_script))[0]

            try:
                try:
                    qid = _json['qid']
                except:
                    qid = _json['id']
                type_ = _json['answer']['type']
                qnum = FIND_DIGIT_REGEX.findall(QNUM_REGEX.findall(current_question_script)[0])[0]  
                ansMethordType = 1
                return ansMethordType, {'qid': qid, 'qnum': qnum}, type_
            except:
                params = str(_json['params'])
                params = params.replace('\'', '"').replace('None', 'null').replace('True', 'true').replace('False', 'false')
                permid = _json['permid']
                type_ = _json['answer']['type']
                qnum = FIND_DIGIT_REGEX.findall(QNUM_REGEX.findall(current_question_script)[0])[0]  
                ansMethordType = 2
                return ansMethordType, {'userAnswer': '', 'qnum': qnum, 'permid': permid, 'params': params}, type_
        except (KeyError, IndexError) as e:
            raise NoQuestionFound(e)
    
    @staticmethod
    def parse_V3(questionsRaw: str):
        try:
            data = json.loads(questionsRaw)
            qnum = data['qnum']
            question = data['question']
            
            try:
                qid = question['qid']
                type_ = question['answer']['type']  
                ansMethordType = 1
                return ansMethordType, {'qid': qid, 'qnum': qnum}, type_
            except:
                params = str(question['params'])
                params = params.replace('\'', '"').replace('None', 'null').replace('True', 'true').replace('False', 'false')
                permid = question['permid']
                type_ = question['answer']['type']
                ansMethordType = 2
                return ansMethordType, {'userAnswer': '', 'qnum': qnum, 'permid': permid, 'params': params}, type_
        except (KeyError, IndexError) as e:
            raise NoQuestionFound(e)

    @staticmethod
    def find_tags(page: str):
        a = BeautifulSoup(page, 'html.parser')
        return a.find_all('script')

    @staticmethod
    def extract_json(string: str):
        pos = 0
        while True:
            match = string.find('{', pos)
            if match == -1:
                break
            try:
                result, index = JSONDecoder().raw_decode(string[match:])
                yield result
                pos = match + index
            except ValueError:
                pos = match + 1
