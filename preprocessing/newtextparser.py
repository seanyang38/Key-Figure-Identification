import csv
import re
import sys

rel_path = './keyfigure_text.csv'

rows = []
extract = []

# set csv size and avoid Overflow Error
maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True

# read file
with open(rel_path, encoding='utf-8') as file:
    reader = csv.reader(file, delimiter = "\t")
    count = 0

    for row in reader:
        rows.append(row)

        count += 1

        #if count == 5000: break # break after number of iterations for testing

allpmcids = set()

for r in rows:
    pmcid = r[0]
    sectionID = r[1]
    sectionHeading = r[2]
    sectionText = r[3]

    allpmcids.add(pmcid)

    sectionText = sectionText.replace('\u2009', " ")
    sectionText = sectionText.replace('\xa0', " ")
    sectionText = sectionText.replace('\n', " ")

    sectionTextArr = sectionText.split(" ") 

    #if pmcid == "28985": print(sectionTextArr)

    for i in range(0, len(sectionTextArr) - 1):
        word = sectionTextArr[i] 

        if "Fig" in word or "Table" in word or "Diagram" in word:
            secondword = sectionTextArr[i+1]

            word = re.sub(r'[^0-9a-zA-Z]','', word)
            secondword = re.sub(r"[\(\[].*?[\)\]]", "", secondword)
            #secondword = re.sub(r'[^0-9a-zA-Z]','', secondword)
            secondword = re.sub(r'[^0-9a-zA-Z -]','', secondword) 

            if "Fig" or "Figure" in word:
                word = "Figure"
            elif "Table" in word:
                word = "Table"
            elif "Diagram" in word:
                word = "Diagram"

            if any(char.isdigit() for char in secondword):
                extract.append([pmcid, sectionID, sectionHeading, word, secondword])

            if i+2 < len(sectionTextArr):
                thirdword = re.sub(r'[^0-9a-zA-Z -]','', sectionTextArr[i+2])

                if thirdword == "and":
                    fourthword = re.sub(r"[\(\[].*?[\)\]]", "", sectionTextArr[i+3])
                    fourthword = re.sub(r'[^0-9a-zA-Z -]','', fourthword)

                    if any(char.isdigit() for char in fourthword):
                        extract.append([pmcid, sectionID, sectionHeading, word, fourthword])


def export(data):
    try:
        with open("newfigdata.csv", 'w', newline='', encoding='utf-8') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

            wr.writerow(["PMCID", "SectionID", "SectionHeading", "FigureType", "FigureID"])
            wr.writerows(data)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Attempt export with new name:")

        with open("newfigdata.csv", 'w', newline='', encoding='utf-8') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

            wr.writerows(data)

print(len(list(allpmcids)))

export(extract) # write csv with extracted data