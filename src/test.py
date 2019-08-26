from core import LexIntents
from core import LexSlot
from core import FaqData
from os import system, name

from colorama import Fore, Back, Style

faqSeachEngine = FaqData("template/qa.csv")
slots = LexIntents(faqSeachEngine)
intents = LexSlot(faqSeachEngine)

def doAutomatedTest():
    i = 0

    for question in faqSeachEngine.questionAnswersDict.keys():
        i = i + 1
        ansInFile = faqSeachEngine.questionAnswersDict.get(question)
        ans = faqSeachEngine.findAnswer(question)
        if ansInFile != ans:
            print(Fore.RED + "Failed ID=[{}] Question=[{}] | Expected-Answer=[{}] | Real-Answer=[{}] ".format(i, question, ansInFile, ans))
        else:
            print(Fore.GREEN + "PASSED ID=[{}] Question=[{}] | Expected-Answer=[{}] | Real-Answer=[{}] ".format(i ,question, ansInFile, ans))


def doManualTest():
    quest = ""
    while(quest.lower() != "quit"):
        system('cls')
        quest = input(Fore.CYAN +"Your question (type 'quit' to exit) : ")
        ans = faqSeachEngine.findAnswer(quest)
        print (Fore.LIGHTBLUE_EX + "********[ QUESTION=>{}:      ANSWER=>{} ]".format(quest, ans))
        print (Fore.BLACK + "-----------------")

if (input("Run Automated Test: YES | NO : ").lower() == "yes"):
    doAutomatedTest()
else:
    doManualTest()