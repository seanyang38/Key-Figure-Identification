import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import glob

folder = 'False'
false_filePath_list = glob.glob(folder + '/*')
true_filePath_list = glob.glob('dendrogram/*')
# print filePath_list
# for filePath in filePath_list:
# 	print filePath
# 	image = cv.imread(filePath,0)
# 	height, width = image.shape
# 	if height != 224 and width != 224:
# 		newImage = np.zeros((224, 224), dtype=np.uint8)
# 		if height > width:
# 			ratio = float(224)/height
# 		else:
# 			ratio = float(224)/width
# 		scaled_image = cv.resize(image, (0,0), fx = ratio, fy=ratio)
# 		n_height, n_width = scaled_image.shape
# 		h_offset = (224 - n_height) / 2
# 		w_offset = (224 - n_width) / 2
# 		newImage[h_offset:h_offset+n_height,w_offset:w_offset+n_width] = scaled_image


# 		cv.imwrite(filePath, newImage)

for i, filepath in enumerate(false_filePath_list):
	if i%10 == 0:
		with open('val.txt', 'ab') as f:
			f.write(filepath + ' 0' +  '\n')
	elif i%10 == 1:
		with open('test.txt', 'ab') as f:
			f.write(filepath +' 0' +  '\n')
	else:
		with open('train.txt', 'ab') as f:
			f.write(filepath +' 0' +  '\n')

for i, filepath in enumerate(true_filePath_list):
	if i%10 == 0:
		with open('val.txt', 'ab') as f:
			f.write(filepath +' 1' + '\n')
	elif i%10 == 1:
		with open('test.txt', 'ab') as f:
			f.write(filepath +' 1' + '\n')
	else:
		with open('train.txt', 'ab') as f:
			f.write(filepath +' 1' + '\n')
	