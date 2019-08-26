import csv
import json
import re

def main():
    processSlotTypes()

def excludeCheck(keyword):
    excludes = ['/', 'I', 'do', 'a', 'am', 'of', 'are', 'my', 'if', 'the', 'is', 'will']
    for k in excludes:
        # print (k)
        if k.lower() == keyword.lower():
            return False
    return True

def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

def processSlotTypes():
    csvFile = open('template.csv', 'r')
    jsonFile = open('file.json', 'w')
    keywords = []
    fieldnames = ("Question")
    reader = csv.DictReader( csvFile, fieldnames)

    # for row in reader:
    #     keywords.append(row)
    #     # print(row);
    #     # json.dump(row, jsonfile)
    #     # jsonfile.write('\n')

    with open("template.csv") as f:
        list = [line.split() for line in f]        # create a list of lists

        for i, x in enumerate (list):               # print the list items
            # print ("line{0} = {1}".format(i, x))
            for k in x:
                if excludeCheck(k):
                    cleanString = re.sub('\W+','', k)
                    cleanString = re.sub(r'\b\d+(?:\.\d+)?\s+', '', cleanString)
                    keywords.append(cleanString)

    # keywords = list(dict.fromkeys(keywords))
    keywords = Remove(keywords)

    for keyword in keywords:
        print (keyword)

main()