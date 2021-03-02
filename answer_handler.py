import functools
import json
import sys
from statistics import mean

from parser_utils import Parser, NoQuestionFound, AAID_REGEX, FIND_DIGIT_REGEX


class InvalidURLException(BaseException):
    def __init__(self, url, *args):
        self.__url = url
        super().__init__(*args)

    def __str__(self):
        return f"Invalid URL {self.__url}"


def catch(func):
    @functools.wraps(func)
    def stub(self, *args, **kwargs):
        try:
            return func(self, *args, *kwargs)
        except NoQuestionFound:  # raised in parser, questions finished
            return True, True
        except KeyboardInterrupt:
            sys.exit()  # quits script
        except BaseException as e:
            return None, e

    return stub


class AnswerHandler:
    def __init__(self, session):
        self.sesh = session
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/87.0.4280.141 Safari/537.36'}
        self.process_ans_url = 'https://www.drfrostmaths.com/process-answer-new.php'
        self.process_skip_url = 'https://www.drfrostmaths.com/process-skipquestion2.php'
        self.answer_functions = {
                                 'numeric': self.answer_numeric,
                                 'expression': self.answer_expression,
                                 'eqnsolutions': self.answer_eqnsolutions,
                                 'coordinate': self.answer_coordinate,
                                 'multiplechoice': self.answer_multiplechoice,
                                 'textual': self.answer_textual,
                                 'fraction': self.answer_fraction,
                                 'vector': self.answer_vector,
                                 'table': self.answer_table,
                                 'shape': self.answer_shape,
                                 'list': self.answer_list,
                                 'standardform': self.answer_standardform,
                                 'desmos_line': self.answer_desmosLine}


    def find_answer(self, data: dict, type_: str):
        data = dict(data)
        data[f'{type_}-answer-1'] = '1'  # prepare incorrect  answer
        print(f'Question number: {data["qnum"]}', '|', f'Question type: {type_}')
        r = self.sesh.post(self.process_ans_url, data=data, headers=self.headers)  # submit incorrect answer
        _json = json.loads(r.text)
        return _json['answer']  # parse correct answer


    @staticmethod
    def new_type(answer: dict, type_: str):
        print(f'Type:{type_})'
              f'\n {answer}')

    @staticmethod
    def wrong_answer(response, data: dict):
        print('-- The wrong answer was submitted --')
        print('The following data if for debugging:')
        print(f'Request: {data}')
        print(f'Response: {response}')

    @catch
    def answer_questions_V3(self, url: str, submit=True):
        try:
            aaid = FIND_DIGIT_REGEX.findall(AAID_REGEX.findall(url)[0])[0]
        except IndexError:
            raise InvalidURLException(url)

        while True:
            page = self.sesh.get(url, headers=self.headers, verify=False).text
            ansMethordType, data, type_ = Parser.parse_V2(page)

            if ansMethordType == 1:
                answer = self.find_answer_qid(data, type_)
            elif ansMethordType == 2:
                answer = self.find_answer_params(data, type_)

            data['aaid'] = aaid

            try:
                result = self.answer_functions[type_](data, answer)  # select appropriate function to process answer
            except KeyError:
                self.new_type(answer, type_)  # not implemented type
                continue  # skips auto submit

            self.submit(result)
    @catch
    def answer_question_V3(self, url: str, submit: bool):
        try:
            aaid = FIND_DIGIT_REGEX.findall(AAID_REGEX.findall(url)[0])[0]
        except IndexError:
            raise InvalidURLException(url)
        page = self.sesh.get(url, headers=self.headers, verify=False).text
        ansMethordType, data, type_ = Parser.parse_V2(page)

        if ansMethordType == 1:
            answer = self.find_answer_qid(data, type_)
        elif ansMethordType == 2:
            answer = self.find_answer_params(data, type_)

        data['aaid'] = aaid

        if submit:
            try:
                result = self.answer_functions[type_](data, answer)  # select appropriate function to process answer
            except KeyError:
                self.new_type(answer, type_)  # not implemented type
                return True, True
            
            self.submit(result)

        print(f'Answer: {self.beautify_Answer(answer)}\n')
        return True, False
        
            

    def find_answer_qid(self, data: dict, type_: str):
        print(f'Question number: {data["qnum"]}', '|', f'Question type: {type_}')
        data = dict(data)
        data['userAnswer'] = '"1"'
        
        r = self.sesh.post(self.process_ans_url, headers=self.headers, data=data)

        _json = json.loads(r.text)
        
        return _json['answer'] 
        
    
    def find_answer_params(self, data: dict, type_: str):
        print(f'Question number: {data["qnum"]}', '|', f'Question type: {type_}')
        data = dict(data)
        test = dict()
        data['userAnswer'] = "1"
        
        r = self.sesh.post(self.process_ans_url, headers=self.headers, data=data)
        _json = json.loads(r.text)
        
        return _json['answer'] 
        

    def submit(self, data: dict):
        try:
            r = self.sesh.post(self.process_ans_url, headers=self.headers, data=data, timeout=3, verify=False)
        except BaseException:
            return False
        
            
    def beautify_Answer(self, answer):
        try:
            answer = answer['main'].replace("'",'"').replace('\\left',  "").replace('\\right',  "")
            return answer
        except:
            return answer

    
    def answer_numeric(data, answer):
        temp=[]
        for index, item in enumerate(answer):
            try:
                if item['exact']:
                    temp.append(str(item['exact']))
                    data['userAnswer'] = json.dumps(temp)
                else:
                    # find mid value
                    temp.append(str(mean([float(item["to"]), float(item["from"])])))
                    data['userAnswer'] = json.dumps(temp)
            except:
                temp.append(str(mean([float(item["to"]), float(item["from"])])))
                data['userAnswer'] = json.dumps(temp)
        return data
    


    @staticmethod
    def new_type(answer: dict, type_: str):
        print(f'No system in place to auto submit this answer type ({type_}) you will have to type it in manually then rerun this:'
              f'\n {answer}')
        



    @staticmethod
    def answer_expression(data, answer):
        answer = [answer['main']]
        data['userAnswer'] = '"' + str(answer[0]).replace("'",'"').replace('\\times',  "\\\\times").replace('\\frac',  "\\\\frac").replace('\\sqrt',  "\\\\sqrt").replace('\\left',  "\\\\left").replace('\\right',  "\\\\right").replace('\\le', "\\\\le") + '"'
        return data



    @staticmethod
    def answer_eqnsolutions(data, answer):
        data['userAnswer'] = json.dumps(answer)
        return data

    @staticmethod
    def answer_coordinate(data, answer):
        data['userAnswer'] = json.dumps(answer)
        return data

    @staticmethod
    def answer_multiplechoice(data, answer):
        data['userAnswer'] = json.dumps(answer)
        return data

    @staticmethod
    def answer_textual(data, answer):
        temp2 = []
        for part in answer:
            temp = []
            if type(part) is str:
                temp = part.split(' OR ')
            else:
                temp.append(part)
            temp2.append(temp[0])
        data['userAnswer'] = json.dumps(temp2)
        return data

    @staticmethod
    def answer_fraction(data, answer):
        data['userAnswer'] = json.dumps(answer)
        
        return data

    @staticmethod
    def answer_vector(data, answer):
        data['userAnswer'] = json.dumps(answer)
        return data

    @staticmethod
    def answer_table(data, answer):
        data['userAnswer']=json.dumps(answer)
        return data

    @staticmethod
    def answer_shape(data, answer):
        data['userAnswer'] = json.dumps(answer)
        return data

    @staticmethod
    def answer_list(data, answer):
        data['userAnswer'] = json.dumps(answer)
        return data

    @staticmethod
    def answer_standardform(data, answer):
        data['userAnswer'] = json.dumps(answer)
        return data

    @staticmethod
    def answer_desmosLine(data, answer):
        data['userAnswer'] = json.dumps(answer)
        return data