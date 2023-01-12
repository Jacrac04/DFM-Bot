from requests import Session

DFM_NEXT_QUESTION_URL = "https://www.drfrostmaths.com/api/tasks/question/get"

class Questions:
    def __init__(self, aaid: int, session: Session):
        self.aaid = aaid
        self.session = session

    def get_next_question(self):
        res = self.session.post(DFM_NEXT_QUESTION_URL, json={"aaid": self.aaid}).json()
        question = res["question"]
        return res["qnum"], question["qid"], question["answer"]["type"]  # qnum, qid, type
