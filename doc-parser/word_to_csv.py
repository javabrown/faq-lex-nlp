import docx

doc = docx.Document("sample.docx")
key = ''
value = ''

for i in doc.paragraphs:
    if key == '':
        key = i.text
    else:
        value = i.text

    if key and value:
        print( "{} --> {}\n\n".format(key, value) )
        key = ''
        value = ''
        print ("-----------------------------------")
