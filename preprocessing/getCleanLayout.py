import csv
import numpy as np

heading_keywords = ['result', 'discussion', 'method', 'case', 'material', 'implementation', 'design', 'content', 'model', 'experiment']

def getOneHotHeading(heading):
	heading = heading.lower()

	onehot = np.zeros(len(heading_keywords), dtype = np.int64)
	for idx, word in enumerate(heading_keywords):
		if word in heading:
			onehot[idx] = 1

	return list(onehot)
csvReader = csv.reader(open('layout_feature_raw_test.csv', 'r'), delimiter = ',')
csvWriter = csv.writer(open('layout_feature_clean_test.csv', 'a'), delimiter = ',', quoting=csv.QUOTE_ALL)
csvWriter.writerow(['pmcid', 'img_name', 'section_ratio', 'img_order'] + heading_keywords)
onn = []
for row in csvReader:
	data = row[:2] + [row[4], row[7]]
	onehot_feature = getOneHotHeading(row[5])
	data += onehot_feature

	csvWriter.writerow(data)


