import json
import core as c

class LexIntents:
    faqs = {}
    jsonData = {}

    def __init__(self, faqsData):
        self.faqs = faqsData #c.FaqData("template/qa.csv")
        self.generate()

    def generate(self):
        with open('template/intents_model.json') as f:
            self.jsonData = json.load(f)
            f.close()

            # for keyword in self.faqs.getKeywords():
            #     self.jsonData["slots"].append({'name': keyword, 'slotType': 'iCWFAQSlotTypes', 'slotTypeVersion':'$LATEST', 'slotConstraint': 'Optional'})

            # for utterance in self.faqs.getUtterances():
            #     self.jsonData["sampleUtterances"].append(utterance)
            self.jsonData["slots"].append({'name': 'question', 'slotType': 'iCWFAQSlotTypes', 'slotTypeVersion':'$LATEST', 'slotConstraint': 'Required'})
            self.jsonData["sampleUtterances"].append("{question}")

        self.generateAndFlush()

    def generateAndFlush(self):
        generatedJsonFile = open('template/gen/intents.json', 'w')
        json.dump(self.jsonData, generatedJsonFile)
        generatedJsonFile.write('\n')
        generatedJsonFile.close()
        print("Intents generated")
