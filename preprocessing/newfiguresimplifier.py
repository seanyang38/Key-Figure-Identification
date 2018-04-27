import csv
import re
import sys

key_figure_data_rel_path = './newfigdata.csv'
keyfiguredatarows = []
parsedkeyfiguredata = []

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

# read key figure data
with open(key_figure_data_rel_path, encoding='utf-8') as file:
    reader = csv.reader(file, delimiter = ",")
    count = 0

    #keyfiguredatarows = sorted(reader, key=operator.itemgetter(0), reverse=True)

    for row in reader:
        keyfiguredatarows.append(row)

        count += 1

        #if count == 5000: break # break after number of iterations for testing

index = 0
pmcid = None
currentFigures = set()
allfigures = set()

for i in range(1,len(keyfiguredatarows)):
    r = keyfiguredatarows[i]

    currPMCID = r[0]

    allfigures.add(currPMCID)

    if pmcid == None:
        pmcid = currPMCID

    if currPMCID != pmcid:
        pmcid = currPMCID
        currentFigures = None
        currentFigures = set()
    
    currFigureID = r[4]

    if not currFigureID.startswith('S') and r[3] == "Figure":
        split = re.findall(r'\d+|D+', currFigureID)
        id = split[0]
            
        if id.isdigit() and id not in currentFigures:
            currentFigures.add(id)

            parsedkeyfiguredata.append([r[0], r[1], r[2], r[3], id])

def export(data, headers, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

        wr.writerow(headers)
        wr.writerows(data)

print(len(list(allfigures)))

export(parsedkeyfiguredata, ["PMCID", "SectionID", "SectionHeading", "FigureType", "FigureID"], 'newsimplefigdata.csv')
