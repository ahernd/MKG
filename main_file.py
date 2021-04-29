import sys
import extract_text_from_pdf as epdf
import extract_text_from_image as eimage
import os
import pandas as pd
import draw_graph as dg

def create_sent_token(filename,input_patient_id):
	outfilename = 'Output/'+input_patient_id+'_Data.csv'
	from nltk import tokenize
	with open(filename,'r') as rb:
		data = rb.read()
	updated_text = tokenize.sent_tokenize(data)
	df = pd.DataFrame(columns=['data'],data=updated_text)
	df.to_csv(outfilename,index=False)
	return outfilename

def main():
	input_patient_id = sys.argv[1]
	operation_mode = 'w'
	input_loc = 'Input/'
	output_file = 'Output/'+input_patient_id+'_content.txt'
	for file in os.listdir(input_loc):
		if file.startswith(input_patient_id+'_'):
			print(file)
			if file.split('.')[1].upper() == 'PDF':
				epdf.extract_text(input_loc+file,operation_mode,output_file)
			elif file.split('.')[1].upper() in  ['JPG','PNG']:
				eimage.extract_text(input_loc+file,operation_mode,output_file)
			else:
				print('no valid input image')
			operation_mode = 'a'	
	outfilename = create_sent_token(output_file,input_patient_id)				
	dg.read_data(outfilename,input_patient_id)
	print('Execution completed')

if __name__ == "__main__":
    main()