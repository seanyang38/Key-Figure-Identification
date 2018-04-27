from shutil import  copy
import os

## TEST IMAGES

script_dir = os.path.dirname(__file__)
rel_path = "train_dendrogram/test.txt"
abs_file_path = os.path.join(script_dir, rel_path)

f = open(abs_file_path)

for i in f.readlines():
    split = i.split()
    binarylabel = split[1]
    relativepath = split[0]

    split2 = split[0].split("/")
    directory = split2[0]
    filename = split2[1]

    if directory == "False":
        copy(os.path.join(script_dir, "train_dendrogram/" + relativepath), os.path.join(script_dir, "data/val/notdend"))    
    else:
        copy(os.path.join(script_dir, "train_dendrogram/" + relativepath), os.path.join(script_dir, "data/val/dend"))    

f.close()

## TRAIN IMAGES

script_dir = os.path.dirname(__file__)
rel_path = "train_dendrogram/train.txt"
abs_file_path = os.path.join(script_dir, rel_path)

f = open(abs_file_path)

for i in f.readlines():
    split = i.split()
    binarylabel = split[1]
    relativepath = split[0]

    split2 = split[0].split("/")
    directory = split2[0]
    filename = split2[1]

    if directory == "False":
        copy(os.path.join(script_dir, "train_dendrogram/" + relativepath), os.path.join(script_dir, "data/train/notdend"))    
    else:
        copy(os.path.join(script_dir, "train_dendrogram/" + relativepath), os.path.join(script_dir, "data/train/dend"))    

f.close()

## VALIDATE IMAGES

script_dir = os.path.dirname(__file__)
rel_path = "train_dendrogram/val.txt"
abs_file_path = os.path.join(script_dir, rel_path)

f = open(abs_file_path)

for i in f.readlines():
    split = i.split()
    binarylabel = split[1]
    relativepath = split[0]

    split2 = split[0].split("/")
    directory = split2[0]
    filename = split2[1]

    if directory == "False":
        copy(os.path.join(script_dir, "train_dendrogram/" + relativepath), os.path.join(script_dir, "data/eval/notdend"))    
    else:
        copy(os.path.join(script_dir, "train_dendrogram/" + relativepath), os.path.join(script_dir, "data/eval/dend"))    

f.close()
