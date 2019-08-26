import math
import datetime
import time
import os
import logging
import json
import re
import json
import re
import csv
import difflib
# from fuzzywuzzy import fuzz

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# -------------------FAQ-------------------

class FaqData:
    keywords = set()
    questions = []
    questionAnswersDict = {}

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
            if reader:
                for row in reader:
                    if(row):
                        # print(row[2])
                        self.questions.append(row[1])
                        self.questionAnswersDict.update({row[1]: row[2]})
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
        excludes = ['how', 'you', 'in', 'your', 'off', 'pay', 'early', 'does', 'do', '/', 'I', 'do', 'a', 'am', 'was', 'of', 'are', 'my', 'if', 'the', 'is', 'will', 'Iâm', 'I\u00e2m', 'I’m', 'have', 'has', 'to', 'much', 'there', 'for', 'can', 'any', 'iâm', 'or','\u00e2']
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


    def findAnswer(self, question):
        possibleAnswerKey = "NO ANSWER"
        activeMatchPoint = -1;

        for key in self.questionAnswersDict:
            matchPoint = self.wordMatchCount(question, key)
            # matchPoint = self.matchRatio(question, key)
            if matchPoint > 0 and matchPoint >= activeMatchPoint:
                activeMatchPoint = matchPoint
                possibleAnswerKey = key;

        if activeMatchPoint > 0:
            print (possibleAnswerKey + " : " + self.questionAnswersDict.get(possibleAnswerKey))
            ans = self.questionAnswersDict.get(possibleAnswerKey)
            # return ans
            return '{}.  [ debug=>match-ratio={}%]'.format(ans, str(activeMatchPoint))

        return "NO ANSWER"

    def  wordMatchCount(self, str1, str2):
        # qset = set(str1.split(' '))
        # i = 0;
        # for subStr in qset:
        #     if str2.lower().find(subStr.lower()) >= 0:
        #         i = i+1
        # return i
        seq = difflib.SequenceMatcher(None, str1, str2)
        d = seq.ratio()*100
        return d

    # def  matchRatio(self, str1, str2):
    #     # qset = set(str1.split(' '))
    #     # i = 0;
    #     # for subStr in qset:
    #     #     if str2.lower().find(subStr.lower()) >= 0:
    #     #         i = i+1
    #     # return i
    #     ratio = fuzz.token_set_ratio(str1, str2)
    #     # d = seq.ratio()*100
    #     return ratio

# ------------------------------------------


class LexEvent:
    """handles incoming and outgoing params to Lex and validates slots"""

    def __init__(self, event):
        self.event = event
        self.slots = event['currentIntent']['slots']
        self.intent = event['currentIntent']['name']
        self.input_text = event['inputTranscript']
        self.sess_attr = event['sessionAttributes']
        self.invocation = event['invocationSource']

    def getUserInputText(self):
        return self.input_text

    def tostr(self):
        return self.input_text + " - "

    ### Helpers to control state of the conversation

    def delegate(self, intent=None):
        return {
            'sessionAttributes': self.sess_attr,
            'dialogAction': {
                'type': 'Delegate',
                'slots': self.slots
            }
        }

    def fulfill(self, msg="Your document is complete."):
        return {
            'sessionAttributes': self.sess_attr,
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Fulfilled',
                "message": {
                    "contentType": "PlainText",
                    "content": msg
                }
            }
        }



    def elicit_slot(self, err):
        return {
            'sessionAttributes': self.sess_attr,
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': self.intent,
                'slots': self.slots,
                'slotToElicit': err['violatedSlot'],
                'message': {'contentType': 'PlainText', 'content': err['message'] }
            }
        }

    def elicit_intent(self, msg="How can I help you?"):
        return {
            "sessionAttributes": self.sess_attr,
            "dialogAction": {
                "type": "ElicitIntent",
                "message": {
                    "contentType": "PlainText",
                    "content": msg
                }
            }
        }

    #### Slot Validators

    def val_error(self, slot, msg):
        res = {"isValid": False, "violatedSlot": slot, 'message': msg }
        return res

    def validates_presence(self, slot, msg=None):
        if not self.slots[slot]: # raise val_error
            if not msg:
                msg = "What is the {}?".format(slot)
            err = self.val_error(slot, msg)
            return self.elicit_slot(err)

    def validates_in(self, iterable, slot, msg=None):
        if self.slots[slot] not in iterable:
            if not msg:
                iter_list = ", ".join([str(x) for x in iterable])
                msg = "Your {0} must be one of the following: {1}".format(slot, iter_list)
            err = self.val_error(slot, msg)
            return self.elicit_slot(err)

    def validates_length(self, rng, slot, msg=None):
        if not self.slots[slot]: return
        # rng = (min, max)
        if len(self.slots[slot]) > rng[1]:
            if not msg:
                msg = "Your {0} is too large. I can handle {1} characters max.".format(slot, rng[1])
            err = self.val_error(slot, msg)
            return self.elicit_slot(err)

        if len(self.slots[slot]) < rng[0]:
            if not msg:
                msg = "Your {0} is too small. I need at least {1} characters.".format(slot, rng[0])
            err = self.val_error(slot, msg)
            return self.elicit_slot(err)


    def validates_pattern(self, regex, slot, msg=None):
        if not self.slots[slot]: return

        pattern = re.compile(regex)
        if not pattern.match(self.slots[slot]):
            if not msg:
                msg = "Your {0} seems to have an invalid format".format(slot)
            err = self.val_error(slot, msg)
            return self.elicit_slot(err)


    def run_validation(self, validators):
        for error in validators:
            if error:
                return error

        return lex.delegate()



#### Intent handlers based on dispatch function


def deliver_document(lex):
    if lex.invocation == "FulfillmentCodeHook":
        return lex.fulfill("Your document has been emailed!")

    validators = [
        lex.validates_presence('emailAddress', "What email address would you like this document sent to?"),
        lex.validates_pattern("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                              "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                              "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)",
                              'emailAddress', ""),
    ]

    return lex.run_validation(validators)


def bill_of_sale(lex):

    if lex.invocation == "FulfillmentCodeHook":
        return lex.fulfill()

    validators = [
        lex.validates_presence('buyer', "What is the buyer's name? "),
        lex.validates_presence('buyerAddress', "What is the buyer's address?"),
        lex.validates_presence('seller', "What is the seller's name?"),
        lex.validates_presence('sellerAddress', "What is the seller's address?"),
        lex.validates_presence('itemSold', "What is the item being sold called? Brand, make, model or name"),
        lex.validates_presence('serial', "What is the serial number? If any"),
        lex.validates_presence('description', "Briefly describe the item or any special characteristics"),
        lex.validates_presence('price', "What is the total final selling price in dollars?, i.e 500 "),
        lex.validates_presence('jurisdiction', "Where should this contract be enforced? Usually it's where the transaction takes place."),
    ]

    return lex.run_validation(validators)

def boat_bill_of_sale(lex):

    if lex.invocation == "FulfillmentCodeHook":
        return lex.fulfill()

    validators = [
        lex.validates_presence('buyer', "What is the name of the person buying the vessel? "),
        lex.validates_presence('buyerAddress', "What is the buyer's address?"),
        lex.validates_presence('seller', "What is the seller's name?"),
        lex.validates_presence('sellerAddress', "What is the seller's address?"),
        lex.validates_presence('itemMake', "What is the boat's make?"),
        lex.validates_presence('itemModel', "What is the boat's model?"),
        lex.validates_presence('year', "What is the boat's year of construction?"),
        lex.validates_presence('serial', "What is the Hull Identification Number (HIN)"),
        lex.validates_presence('price', "What is the total final selling price in dollars?"),
        lex.validates_presence('jurisdiction', "Where should this contract be enforced? Usually it's where the transaction takes place."),
    ]

    return lex.run_validation(validators)

def vehicle_bill_of_sale(lex):

    if lex.invocation == "FulfillmentCodeHook":
        return lex.fulfill()

    validators = [
        lex.validates_presence('buyer', "What is the name of the person buying the vehicle? "),
        lex.validates_presence('buyerAddress', "What is the buyer's address?"),
        lex.validates_presence('seller', "What is the seller's name?"),
        lex.validates_presence('sellerAddress', "What is the seller's address?"),
        lex.validates_presence('itemMake', "What is the vehicle's make?"),
        lex.validates_presence('itemModel', "What is the vehicle's model?"),
        lex.validates_presence('year', "What year is the vehicle?"),
        lex.validates_presence('itemType', "What type of vehicle is this? Car, Truck, ATV, Hovercraft, etc...?"),
        lex.validates_presence('odometer', "What is the current odometer reading?"),
        lex.validates_presence('serial', "What is the Vehicle Identification Number (VIN)"),
        lex.validates_presence('price', "What is the total final selling price in dollars? "),
        lex.validates_presence('jurisdiction', "Where should this contract be enforced? Usually it's where the transaction takes place."),
    ]

    return lex.run_validation(validators)

def animal_bill_of_sale(lex):

    if lex.invocation == "FulfillmentCodeHook":
        return lex.fulfill("Your animal bill of sale is complete!")

    validators = [
        lex.validates_presence('buyer', "What is the name of the person buying the animal? "),
        lex.validates_presence('buyerAddress', "What is the buyer's address?"),
        lex.validates_presence('seller', "What is the seller's name?"),
        lex.validates_presence('sellerAddress', "What is the seller's address?"),
        lex.validates_presence('itemType', "What type of animal is being sold? Dog, Cat, Snake, Turtle, etc."),
        lex.validates_presence('itemMake', "What is the animal's breed?"),
        lex.validates_presence('year', "What year was the animal born?"),
        lex.validates_presence('color', "What color is the animal?"),
        lex.validates_presence('serial', "What is the animal's ID or chip number, if any?"),
        lex.validates_presence('description', "Briefly describe any other important details"),
        lex.validates_presence('price', "What is the total final selling price in dollars?"),
        lex.validates_presence('jurisdiction', "Where should this contract be enforced? Usually it's where the transaction takes place."),
    ]

    return lex.run_validation(validators)

def firearm_bill_of_sale(lex):

    if lex.invocation == "FulfillmentCodeHook":
        return lex.fulfill()

    validators = [
        lex.validates_presence('buyer', "What is the name of the person buying the firearm? "),
        lex.validates_presence('buyerAddress', "What is the buyer's address?"),
        lex.validates_presence('seller', "What is the seller's name?"),
        lex.validates_presence('sellerAddress', "What is the seller's address?"),
        lex.validates_presence('itemMake', "What is the firearm make or manufacturer?"),
        lex.validates_presence('itemModel', "What is the firearm model?"),
        lex.validates_presence('itemType', "What is the firearm caliber?"),
        lex.validates_presence('serial', "What is the firearm's serial number?"),
        lex.validates_presence('price', "What is the total final selling price in dollars?"),
        lex.validates_presence('jurisdiction', "Where should this contract be enforced? Usually it's where the transaction takes place."),
    ]

    return lex.run_validation(validators)

def general_contract(lex):

    if lex.invocation == "FulfillmentCodeHook":
        return lex.fulfill()

    validators = [
        lex.validates_presence('provider', "What is the name of the Promisor or Provider in the contract?"),
        lex.validates_presence('providerAddress', "What is the Promisor's address?"),
        lex.validates_presence('receiver', "What is the Promisee's name?"),
        lex.validates_presence('receiverAddress', "What is the Promisee's address?"),
        lex.validates_presence('description', "What are the terms of your contract? Describe the legal relationship between the promisor and promisee."),
        lex.validates_presence('jurisdiction', "Where should this contract be enforced? Usually it's where the transaction takes place.")
    ]

    return lex.run_validation(validators)

def pool_service_contract(lex):

    if lex.invocation == "FulfillmentCodeHook":
        return lex.fulfill()

    validators = [
        lex.validates_presence('provider', "What is the name of the person or company providing pool services?"),
        lex.validates_presence('providerAddress', "What is the provider's address?"),
        lex.validates_presence('receiver', "What is the client's name?"),
        lex.validates_presence('receiverAddress', "What is the client's address?"),
        lex.validates_presence('interval', "How often will the client be billed? Monthly, Yearly, etc."),
        lex.validates_presence('rate', "How much will be charged per billing cycle in dollars?"),
        lex.validates_presence('frequency', "How often will pool services be conducted? Weekly, Monthly, etc."),
        lex.validates_presence('description', "What type of services will be offered? Chemical balancing, filter backwashing, debris skimming, etc."),
        lex.validates_presence('jurisdiction', "Where should this contract be enforced? Usually it's where the transaction takes place."),
    ]

    return lex.run_validation(validators)


def promissory_note(lex):

    if lex.invocation == "FulfillmentCodeHook":
        return lex.fulfill()

    validators = [
        lex.validates_presence('provider', "What is the name of the person or company lending money?"),
        lex.validates_presence('providerAddress', "What lender's address?"),
        lex.validates_presence('receiver', "What is the borrower's name?"),
        lex.validates_presence('receiverAddress', "What is the borrower's address?"),
        lex.validates_presence('principal', "What is the principal balance of the loan?"),
        lex.validates_presence('interest', "What is the interest rate as a percent? "),
        lex.validates_presence('payment', "What is the payment amount per period?"),
        lex.validates_presence('periods', "How many months will the loan last?"),
        lex.validates_presence('startDate', "What date will interest start accruing?"),
        lex.validates_presence('itemSold', "What is the borrower's consideration? In other words, what is this loan for? i.e $5000 cash, Motorcycle, Consulting Services, etc."),
        lex.validates_presence('jurisdiction', "Where should this contract be enforced? Usually it's where the transaction takes place."),
    ]

    return lex.run_validation(validators)

def due_on_demand_note(lex):

    if lex.invocation == "FulfillmentCodeHook":
        return lex.fulfill()

    validators = [
        lex.validates_presence('provider', "What is the name of the person or company lending money?"),
        lex.validates_presence('providerAddress', "What lender's address?"),
        lex.validates_presence('receiver', "What is the borrower's name?"),
        lex.validates_presence('receiverAddress', "What is the borrower's address?"),
        lex.validates_presence('principal', "What is the principal balance of the loan?"),
        lex.validates_presence('interest', "What is the interest rate?"),
        lex.validates_presence('itemSold', "What is this loan for? i.e $5000 cash, Motorcycle, Consulting Services, etc."),
        lex.validates_presence('jurisdiction', "Where should this contract be enforced? Usually it's where the transaction takes place."),
    ]

    return lex.run_validation(validators)



def help_user(lex):
    return lex.fulfill("Start by telling me what type of legal document you need? Such as 'bill of sale', 'promissory note', 'pool service contract', etc. Or you can say 'show all'")

def show_documents(lex):
    return lex.fulfill("Here's the full list of documents I can draft. Which one would you like to get started?")

def not_understood(lex):
    return lex.fulfill("I did not understand that... Can you rephrase your message?")

def developer_info(lex):
    return lex.fulfill("I owe my inception to JeffDelaney.me. Contact him with your questions.")



def dispatch(lex):
    """Routes conversation based on incoming intent"""

    if lex.intent == "BasicHelp":
        return help_user(lex)
    if lex.intent == "ShowDocuments":
        return show_documents(lex)
    if lex.intent == "DeveloperInfo":
        return developer_info(lex)
    if lex.intent == "DeliverDocument":
        return deliver_document(lex)
    if lex.intent == "BillOfSale":
        return bill_of_sale(lex)
    if lex.intent == "BoatBillOfSale":
        return boat_bill_of_sale(lex)
    if lex.intent == "VehicleBillOfSale":
        return vehicle_bill_of_sale(lex)
    if lex.intent == "AnimalBillOfSale":
        return animal_bill_of_sale(lex)
    if lex.intent == "FirearmBillOfSale":
        return firearm_bill_of_sale(lex)
    if lex.intent == "DueOnDemandNote":
        return due_on_demand_note(lex)
    if lex.intent == "PromissoryNote":
        return promissory_note(lex)
    if lex.intent == "GeneralContract":
        return general_contract(lex)
    if lex.intent == "PoolServiceContract":
        return pool_service_contract(lex)
    else:
        return not_understood(lex)

# ---------------MAIN()---------------------
def lambda_handler(event, context=None):
    lex = LexEvent(event)
    logger.info(('IN', event))

    try:
        # res = dispatch(lex)

        faq = FaqData("metainfo/qa.csv")
        # res = lex.fulfill("Hello from lambda - " + lex.tostr() + " - " + faq.questions[2])
        res = lex.fulfill( faq.findAnswer(lex.getUserInputText()) + " | [intent:"+lex.intent + "]" )
        # res = lex.fulfill( "intent="+lex.intent + " | answer:" +  faq.findAnswer( lex.getUserInputText() ) )
        logger.info(('OUT', res))
        return res
    except Exception as e:
        logger.error(e)




# faq = FaqData("metainfo/qa.csv")
# print("Hello from lambda - " +   " - " + faq.questions[2])
# print ( faq.findAnswer("borrow") )

# seq=difflib.SequenceMatcher(None, "qualify", "do I qualify for a loan?")
# d=seq.ratio()*100
# print (d)
#
# seq=difflib.SequenceMatcher(None, "I for a", "do I qualify for a loan?")
# d=seq.ratio()*100
# print (d)

# print ("-->{}".format(faq.findAnswer("How to apply a loan")))