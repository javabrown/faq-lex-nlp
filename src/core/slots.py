import json
import core as c;

class LexSlot:
    faqs = {}
    jsonData = {}

    def __init__(self,  faqsData):
        self.faqs = faqsData #c.FaqData("template/qa.csv")
        self.generate()
        print(self.faqs.getKeywords().__len__())

    def generate(self):
        with open('template/slots_model.json') as f:
            self.jsonData = json.load(f)
            f.close()

            # for keyword in self.faqs.getKeywords():
            #     self.jsonData["enumerationValues"].append({'value': keyword})
            for question in self.faqs.questions:
                self.jsonData["enumerationValues"].append({'value': question})

        self.generateAndFlush()

    def generateAndFlush(self):
        generatedJsonFile = open('template/gen/slots.json', 'w')
        json.dump(self.jsonData, generatedJsonFile)
        generatedJsonFile.write('\n')
        generatedJsonFile.close()
        print("slot-types generated")