class Faq:
    question = ""
    amswer = ""
    keywords = 0

    def __init__(self, question, answer, keywords):
        self.question = question
        self.amswer = answer
        self.keywords = keywords

    def toString(self):
        print("{}:{}:{}".format(self.question, self.amswer, self.keywords))