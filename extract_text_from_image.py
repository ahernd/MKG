from PIL import Image
import pytesseract
import argparse
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#output_file = 'Output/file_content.txt'
def extract_text(i_filename,i_operation_mode,i_output_file):
	# load the example image and convert it to grayscale
	args = {"image":"","preprocess":""}
	args["image"] = i_filename
	args["preprocess"] == "thresh"
	image = cv2.imread(args["image"])
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	 
	# check to see if we should apply thresholding to preprocess the
	# image
	if args["preprocess"] == "thresh":
		gray = cv2.threshold(gray, 0, 255,
			cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	 
	# make a check to see if median blurring should be done to remove
	# noise
	elif args["preprocess"] == "blur":
		gray = cv2.medianBlur(gray, 3)
	 
	# write the grayscale image to disk as a temporary file so we can
	# apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	# load the image as a PIL/Pillow image, apply OCR, and then delete
	# the temporary file
	text = pytesseract.image_to_string(i_filename,lang="eng")
	os.remove(filename)
	with open('file_content.txt','w') as wb:
			wb.write(text)
			
	file1 = open('file_content.txt', 'r')
	Lines = file1.readlines()
	updated_text = ''
	for line in Lines:
		if line[0] == ' ':
			updated_text = updated_text + ' '
			#print(True)
		else: 
			#print(False)
			for i in line.rstrip("\n"):
				if i == '.':
					updated_text = updated_text + str(i) +' '
				else:
					updated_text = updated_text + str(i)
			updated_text = updated_text + ' '                    
			#print('line = ', updated_text)
	updated_text = updated_text + '\n\n'
	with open(i_output_file,i_operation_mode) as wb:
		wb.write(updated_text)
	#from nltk import tokenize
	#updated_text = tokenize.sent_tokenize(text)

	#with open(output_file,'w') as a:
	#	a.write(updated_text)

	return True