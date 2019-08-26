import re
import csv
import difflib
# import pandas as pd
from fuzzywuzzy import fuzz
import core as c

class FaqData:
    keywords = set()
    questions = []
    questionAnswersDict = {}
    qaDict = {}

    templateFileName = ""

    def __init__(self, templateName):
        self.templateFileName = templateName
        self.loadQuestions()
        self.extractKeywords()
        print("FaqData instance created")

    def loadQuestions(self):
        with open(self.templateFileName, 'r', errors='ignore') as csvFile:
            # print(csvFile)
            reader = csv.reader(csvFile)
            rowId = 0

            if reader:
                for row in reader:
                    rowId = rowId + 1
                    if(row and rowId > 1):
                        self.questions.append(row[1])
                        self.questionAnswersDict.update({row[1]: row[2]})
                        if (row[1] and row[2] and row[3]):
                           obj  = c.Faq(row[1],  row[2], row[3])
                           self.qaDict.update({row[1]: obj})
                           # obj.toString()

        csvFile.close()

    def extractKeywords(self):
        for question in self.questions:
            keywords = question.split()
            # print (keywords)
            # for i, x in enumerate (keywords):
            # print ("line{0} = {1}".format(i, x))
            for k in keywords:
                if self.excludeCheck(k):
                    cleanString = re.sub('\W+','', k)
                    cleanString = re.sub(r'\b\d+(?:\.\d+)?\s+', '', cleanString)
                    self.keywords.add(cleanString)


    def extractKeywords0(self):
        with open (self.templateFileName) as f:
            list = [line.split() for line in f]        # create a list of lists

            for i, x in enumerate (list):               # print the list items
                # print ("line{0} = {1}".format(i, x))
                for k in x:
                    if self.excludeCheck(k):
                        cleanString = re.sub('\W+','', k)
                        cleanString = re.sub(r'\b\d+(?:\.\d+)?\s+', '', cleanString)
                        self.keywords.append(cleanString)
        f.close()

    def excludeCheck(self, keyword):
        excludes = []#['how', 'you', 'in', 'your', 'off', 'pay', 'early', 'does', 'do', '/', 'I', 'do', 'a', 'am', 'was', 'of', 'are', 'my', 'if', 'the', 'is', 'will', 'Iâm', 'I\u00e2m', 'I’m', 'have', 'has', 'to', 'much', 'there', 'for', 'can', 'any', 'iâm', 'or','\u00e2']
        for k in excludes:
            # print (k)
            if k.lower() == keyword.lower():
                return False

        return True


    def filterDuplicate(self, duplicate):
        final_list = []
        for val in duplicate:
            if val.lower() not in final_list:
                final_list.append(val.lower())
        return final_list

    def filterNumber(self, list):
        my_list = [item for item in list if item.isalpha()]
        return my_list

    def getKeywords(self):
        # print("Before filter keyword count:" , self.keywords.__len__())
        self.keywords = self.filterDuplicate(self.keywords)
        self.keywords = self.filterNumber(self.keywords)
        # print("After filter keyword count:" , self.keywords.__len__())
        return (self.keywords)

    def replaceWithSlotKey(self, question):
        replacedQuestion = ""
        keywords = self.getKeywords()

        for i, splitedQuestion in enumerate (question.split()):               # print the list items
            # print ("line{0} = {1}".format(i, splitedQuestion))

            splitedQuestion = re.sub('\W+','', splitedQuestion) #cleaning
            splitedQuestion = re.sub(r'\b\d+(?:\.\d+)?\s+', '', splitedQuestion) #cleaning

            for keyword in keywords:
                if (splitedQuestion == keyword):
                    splitedQuestion = splitedQuestion.replace(keyword, "{" + keyword +"}")
                    # print ("removing : " + keyword)
                    if keyword in keywords:
                        keywords.remove(keyword)
                    break

            replacedQuestion = replacedQuestion + " " + splitedQuestion

        print (replacedQuestion.strip())
        return replacedQuestion.strip()


    def getUtterances(self):
        utteranceSet = set()

        for question in self.questions:
            question = re.sub(r'\b\d+(?:\.\d+)?\s+', '', question) #clean string
            # for keyword in self.getKeywords():
            #     if (question.find(keyword) != -1):
            #         question = question.replace(keyword, "{" + keyword +"}")

            question = self.replaceWithSlotKey(question)
            if question:
                utteranceSet.add(question)

        return (utteranceSet)


    def findAnswer(self, question, debug=False):
        if question.find('debug=') >= 0:
            debug = True
            question = question.replace('debug=', '')

        possibleAnswerKey = "NO ANSWER"
        activeMatchPoint = -1;
        activeWeightage = -1;

        for key in self.questionAnswersDict:
            matchPoint = self.wordMatchCount(question, key)
            # matchPoint = self.matchRatio(question, key)
            # print ("{} : {}".format(key, matchPoint))
            if matchPoint > 0 and matchPoint > activeMatchPoint:
                activeMatchPoint = matchPoint
                # weightage = int(self.qaDict.get(key).weightage)
                # keywords = self.qaDict.get(key).keywords
                # self.qaDict.get(key).toString()
                possibleAnswerKey = key
                print ("Active match point is --> {}    Key:{}".format(activeMatchPoint, possibleAnswerKey))

                # if weightage > 0 and weightage > activeWeightage:
                #     activeWeightage = weightage
                #     possibleAnswerKey = key;
                #     print ("Active weightage is --> {} {}".format(weightage, possibleAnswerKey))

        if activeMatchPoint > 0 and activeMatchPoint >= 70 :
            # print (possibleAnswerKey + " : " + self.questionAnswersDict.get(possibleAnswerKey))
            ans = self.questionAnswersDict.get(possibleAnswerKey)
            # return ans
            if debug == True:
                return '{}   debug=>[match-ratio={}% | question={}]'.format(ans, str(activeMatchPoint), possibleAnswerKey)
            return ans

        return "NO_ANSWER"

    def  wordMatchCount(self, str1, str2):
        # qset = set(str1.split(' '))
        # i = 0;
        # for subStr in qset:
        #     if str2.lower().find(subStr.lower()) >= 0:
        #         i = i+1
        # return i
        # seq = difflib.SequenceMatcher(None, str1, str2)
        # d = seq.ratio()*100
        # return d

    # def  matchRatio(self, str1, str2):
    #     # qset = set(str1.split(' '))
    #     # i = 0;
    #     # for subStr in qset:
    #     #     if str2.lower().find(subStr.lower()) >= 0:
    #     #         i = i+1
    #     # return i

        ratio = fuzz.token_set_ratio(str1.lower(), str2.lower())
        #ratio = fuzz.token_sort_ratio(str1.lower(), str2.lower())
        # d = seq.ratio()*100
        return ratio
