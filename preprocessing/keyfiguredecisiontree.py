import csv
import re
import sys
import numpy as np
from sklearn import tree
import graphviz

import random
# code folder structure: ./preprocessing/
# data folder structure: ./preprocessing/data/layout

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

layout_train_data = []
layout_train_target = []
layout_train_data_full = []

layout_test_data_full = []
layout_test_data = []
layout_test_target = []

'''
key_figure_data = {}

# read key_figures.csv
with open('./data/layout/key_figures.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter = "\t")
    count = 0

    for row in reader:
        if count > 0:
            if row[0] not in key_figure_data:
                key_figure_data[row[0]] = [row[1]]
            else:
                key_figure_data[row[0]].append(row[1])

        count += 1

            #if count == 5: break # break after number of iterations for testing
'''

# read new_layout_feature_clean_train.csv
with open('./data/layout/new_layout_feature_clean_train.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter = ",")
    count = 0
    cnt = 0
    for row in reader:
        if count > 0:
            # layosut_train_data.append([float(r) for r in row[2:]])
            if row[14] =='0':
                if random.random() <0.3:
                    cnt+=1
                    layout_train_data.append([float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]), float(row[10]), float(row[11]), float(row[12]), float(row[13])])
                    layout_train_target.append(float(row[14]))
            else:
                layout_train_data.append([float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]), float(row[10]), float(row[11]), float(row[12]), float(row[13])])
                layout_train_target.append(float(row[14]))                
            layout_train_data_full.append(row)
        count += 1
    print(cnt)
            #if count == 5: break # break after number of iterations for testing

# read new_layout_feature_clean_test.csv
with open('./data/layout/new_layout_feature_clean_test.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter = ",")
    count = 0

    for row in reader:
        if count > 0:
            layout_test_data.append([float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]), float(row[10]), float(row[11]), float(row[12]), float(row[13])])
            layout_test_target.append(float(row[14]))

            layout_test_data_full.append(row)
        count += 1

            #if count == 5: break # break after number of iterations for testing

def export(data, headers, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

        if headers is not None:
            wr.writerow(headers)

        wr.writerows(data)

def decisiontree():
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(layout_train_data, layout_train_target)

    dot_data = tree.export_graphviz(clf, out_file = None, feature_names = ['section_ratio', 'img_order', 'result', 'discussion', 'method', 'case', 'material', 'implementation', 'design', 'content', 'model', 'experiment'])
    graph = graphviz.Source(dot_data)
    graph.render('keyfigure')

decisiontree()
