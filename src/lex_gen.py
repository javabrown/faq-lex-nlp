from core import LexIntents
from core import LexSlot
from core import FaqData

faq = FaqData("template/qa.csv")
slots = LexIntents(faq)
intents = LexSlot(faq)

print("Done!! All slots and intenets generated successfully in --> template/gen directory.")
