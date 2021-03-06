import csv
import re
import sys
import operator

key_figure_order_rel_path = './figuredataorder.csv'
key_figure_data_rel_path = './newsimplefigdata.csv'

keyfigureorderrows = []
keyfiguredatarows = []

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

# read key figure order data

with open(key_figure_order_rel_path, encoding='utf-8') as file:
    reader = csv.reader(file, delimiter = ",")
    count = 0
   
    for row in reader:
        if count > 0 and row[2].isdigit():
            keyfigureorderrows.append([int(row[0]), str(row[1]), int(row[2])])
        
        count += 1

# read key figure data
with open(key_figure_data_rel_path, encoding='utf-8') as file:
    reader = csv.reader(file, delimiter = ",")
    count = 0

    for row in reader:
        if count > 0:
            keyfiguredatarows.append([int(row[0]), row[1], row[2], row[3], int(row[4])])
        
        count += 1

def export(data, headers, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

        if headers is not None:
            wr.writerow(headers)

        wr.writerows(data)

########################################################

# create dictionaries

figureorderdict = {}
figuredatadict = {}

for r in keyfigureorderrows:
    if r[0] in figureorderdict:
        figureorderdict[r[0]].append(r)
    else:
        figureorderdict[r[0]] = [r]

for r in keyfiguredatarows:
    if r[0] in figuredatadict:
        figuredatadict[r[0]].append(r)
    else:
        figuredatadict[r[0]] = [r]

figureorderkeys = list(figureorderdict.keys())
figuredatakeys = list(figuredatadict.keys())

########################################################

# word / phrase frequency distributions
sectionHeadingWordDistribution = {}
sectionHeadingPhraseDistribution = {}

# complete dataset
# ['PMCID', 'FileName', 'SectionID', 'MaxSectionID', 'NormalizedSectionID', 'SectionHeading', 'FigureType', 'FigureID']
finalparsedfiguredata = []

# ['PMCID', 'FileName', 'FigureID']
nomismatchparsedfiguredata = []
numCompleteMatches = 0

numMatches = 0
totalnumberofpmcids = len(list(set(figureorderkeys + figuredatakeys)))
numMismatchs = 0

# figure order data

figureorderuniquerows = []
mismatchfigurorderrows = []
numUniqueFigureOrderPMCIDs = 0

# figure data

figuredatauniquerows = []
mismatchfiguredatarows = []
numUniqueFigureDataPMCIDs = 0

## Parse Figure Order Data

def inFigureDatDict(k, val):
    pmcidData = figuredatadict[k]

    for i in range(0, len(pmcidData)):
        if pmcidData[i][4] == val:
            return True, i
    
    return False, 0

for k in figureorderkeys:
    if k not in figuredatadict:
        figureorderuniquerows.extend(figureorderdict[k])
        numUniqueFigureOrderPMCIDs += 1
    else:
        if len(figureorderdict[k]) != len(figuredatadict[k]):
            mismatchfigurorderrows.extend(figureorderdict[k])
            mismatchfiguredatarows.extend(figuredatadict[k])

            numMismatchs += 1
        
        nomismatch = True
        possMatch = []
        maxSectionID = 0

        for i in range(0, len(figureorderdict[k])):
            cond, dataindex = inFigureDatDict(k, figureorderdict[k][i][2])

            if cond is True:
                currRow = figureorderdict[k][i]
                currSectionID = int(figuredatadict[k][dataindex][1])
                currSectionHeading = figuredatadict[k][dataindex][2]

                # Increment Frequency Counts For Section Heading Phrases
                if currSectionHeading.title() in sectionHeadingPhraseDistribution:
                    sectionHeadingPhraseDistribution[currSectionHeading.title()] = sectionHeadingPhraseDistribution[currSectionHeading.title()] + 1
                else:
                    sectionHeadingPhraseDistribution[currSectionHeading.title()] = 1

                sectionHeadingSplit = currSectionHeading.split(' ')

                # Increment Frequency Counts For Section Heading Words
                for sectionWord in sectionHeadingSplit:
                    if sectionWord.title() in sectionHeadingWordDistribution:
                        sectionHeadingWordDistribution[sectionWord.title()] = sectionHeadingWordDistribution[sectionWord.title()] + 1
                    else:
                        sectionHeadingWordDistribution[sectionWord.title()] = 1

                # Set Maximum Section ID For Current PMCID
                if currSectionID > maxSectionID:
                    maxSectionID = currSectionID

                possMatch.append([currRow[0], currRow[1], currSectionID, -1, -1, figuredatadict[k][dataindex][2], figuredatadict[k][dataindex][3], figuredatadict[k][dataindex][4]])
            else:
                nomismatch = False

        if len(possMatch) > 0:
            # normalize SectionID
            for i in range(0, len(possMatch)):
                currSection = possMatch[i][2]
                possMatch[i][4] = float(currSection / maxSectionID)
                possMatch[i][3] = maxSectionID

            finalparsedfiguredata.extend(possMatch)
            numMatches += 1

        if nomismatch is True:
            nomismatchparsedfiguredata.extend(figureorderdict[k])
            numCompleteMatches += 1

## Parse Figure Data

for k in figuredatakeys:
    if k not in figureorderdict:
        figuredatauniquerows.extend(figuredatadict[k])
        numUniqueFigureDataPMCIDs += 1

########################################################

# print statements
print("Total Number of PMCIDs: ")
print(totalnumberofpmcids)
print("Number of Figure Order PMCIDs: ")
print(len(set(figureorderkeys)))
print("Number of Figure Data PMCIDs: ")
print(len(set(figuredatakeys)))
print(" ")
print("Number of Matched PMCIDs: ")
print(numMatches)
print("Number of Complete Matched PMCIDs: ")
print(numCompleteMatches)
print(" ")
print("Number of Unique Figure Order PMCIDs: ")
print(numUniqueFigureOrderPMCIDs)
print("Number of Unique Figure Data PMCIDs: ")
print(numUniqueFigureDataPMCIDs)
print(" ")
#print("Number of Mismatches: ")
#print(numMismatchs)

#print("Section Heading Phrase Frequency Distribution: ")
#print(str(sectionHeadingPhraseDistribution).encode('utf-8'))
#print(" ")

#print("Section Heading Word Frequency Distribution: ")
#print(str(sectionHeadingWordDistribution).encode('utf-8'))

########################################################

#export(figureorderuniquerows, ['PMCID', 'FileName', 'SectionID', 'SectionHeading', 'FigureType', 'FigureID'], 'newuniquefigureorderdata.csv')

#export(figuredatauniquerows, ['PMCID', 'FileName', 'SectionID', 'SectionHeading', 'FigureType', 'FigureID'], 'newuniquefiguredata.csv')

#export(mismatchfigurorderrows, ['PMCID', 'FileName', 'FigureID'], 'newmismatchfigureorderdata.csv')

#export(mismatchfiguredatarows, ['PMCID', 'SectionID', 'SectionHeading', 'FigureType', 'FigureID'], 'newmismatchfiguredata.csv')

#export(finalparsedfiguredata, ['PMCID', 'FileName', 'SectionID', 'MaxSectionID', 'NormalizedSectionID', 'SectionHeading', 'FigureType', 'FigureID'], 'newcombinedfiguredata.csv')

def exportDict(dict, headers, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        if headers is not None:
            writer.writerow(headers)

        for key, value in dict.items():
            writer.writerow([key, value])
    
exportDict(sectionHeadingPhraseDistribution, ['Phrase', 'Frequency'], 'sectionheadingphrases.csv')
exportDict(sectionHeadingWordDistribution, ['Word', 'Frequency'], 'sectionheadingwords.csv')
