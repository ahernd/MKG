# importing required modules
import PyPDF2
#output_file = 'Output/file_content.txt'
def extract_text(i_filename,i_operation_mode,i_output_file):

	# creating a pdf file object
	pdfFileObj = open(i_filename, 'rb')
		
	# creating a pdf reader object
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
		
	# printing number of pages in pdf file
	print(pdfReader.numPages)
	updated_text = ''

	for num in range(pdfReader.numPages):	
		# creating a page object
		pageObj = pdfReader.getPage(num)
			
		# extracting text from page
		text = pageObj.extractText() 
		#print(text)

		with open('file_content.txt','w') as wb:
			wb.write(text)
			
		file1 = open('file_content.txt', 'r')
		Lines = file1.readlines()

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
				#print('line = ', updated_text)
		updated_text = updated_text + '\n\n'
	#print(updated_text)
	with open(i_output_file,i_operation_mode) as wb:
		wb.write(updated_text)
	# closing the pdf file object
	pdfFileObj.close()
	return True
