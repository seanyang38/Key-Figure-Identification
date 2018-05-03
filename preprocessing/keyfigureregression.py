import csv
import re
import sys
from sklearn.linear_model import LogisticRegression

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

layout_test_data_full = []
layout_test_data = []
layout_test_target = []

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

# read new_layout_feature_clean_train.csv
with open('./data/layout/new_layout_feature_clean_train.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter = ",")
    count = 0

    for row in reader:
        if count > 0:
            layout_train_data.append([float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]), float(row[10]), float(row[11]), float(row[12]), float(row[13])])
            layout_train_target.append(float(row[14]))
        count += 1

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

def create_new_layout_file():
    layout_data = []
    new_layout_data = []
    header = ['pmcid', 'img_name', 'section_ratio', 'img_order', 'result', 'discussion', 'method', 'case', 'material', 'implementation', 'design', 'content', 'model', 'experiment', 'is_key']

    # read layout_feature_clean_test.csv
    with open('./data/layout/layout_feature_clean_test.csv', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter = ",")
        count = 0

        for row in reader:
            if count > 0:
                layout_data.append(row)

            count += 1

                #if count == 5: break # break after number of iterations for testing

    for row in layout_data:
        pmcid = row[0]
        imgname = row[1]

        if pmcid in key_figure_data:
            key_figure_imgs = key_figure_data[pmcid]

            match = False

            for k in key_figure_imgs:
                if imgname == k:
                    match = True
                    break
            
            if match:
                row.append(1)
            else:
                row.append(0)
            
            new_layout_data.append(row)
        else:
            row.append(0)
            new_layout_data.append(row)
    
    export(new_layout_data, header, 'new_layout_feature_clean_test.csv')

# create_new_layout_file()

logistic_model = LogisticRegression()

logistic_model.fit(layout_train_data, layout_train_target)

model_predictions = logistic_model.predict(layout_test_data)

model_score = logistic_model.score(layout_test_data, layout_test_target)

print("MODEL SCORE: %s" % model_score)

if len(layout_test_data_full) == len(model_predictions):
    layout_test_data_full_with_predictions = []
    header = ['pmcid', 'img_name', 'section_ratio', 'img_order', 'result', 'discussion', 'method', 'case', 'material', 'implementation', 'design', 'content', 'model', 'experiment', 'is_key', 'prediction', 'accurate']

    num_pos_count = 0
    num_pos_accurate = 0

    num_neg_count = 0
    num_neg_accurate = 0

    for i in range(0, len(layout_test_data_full)):
        count += 1

        curr_row = layout_test_data_full[i]
        prediction = model_predictions[i]

        accuracte = 0

        if float(curr_row[14]) == float(prediction):
            accuracte = 1
        
        if float(curr_row[14]) == 1:
            num_pos_count += 1
            if float(prediction) == 1:
                num_pos_accurate += 1
        elif float(curr_row[14]) == 0:
            num_neg_count += 1
            if float(prediction) == 0:
                num_neg_accurate += 1

        new_row = curr_row
        new_row.append(prediction)
        new_row.append(accuracte)

        layout_test_data_full_with_predictions.append(new_row)

    print("Positive Prediction Accuracy: %s Percent" % ((num_pos_accurate / num_pos_count)*100))
    print("Negative Prediction Accuracy: %s Percent" % ((num_neg_accurate / num_neg_count)*100))

    export(layout_test_data_full_with_predictions, header, 'predicted_layout_feature_clean_test.csv')
