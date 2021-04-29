import re
import pandas as pd
import bs4
import requests
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

from spacy.matcher import Matcher 
from spacy.tokens import Span 

import networkx as nx

import matplotlib.pyplot as plt
from tqdm import tqdm

pd.set_option('display.max_colwidth', 200)

def read_data(filename,patientid):
	print(filename)
	candidate_sentences = pd.read_csv(filename)
    # import csv sentence file which is output of text extraction
	# Now we can use this function to extract these entity pairs for all the sentences in our data:
	entity_pairs = []

	for i in (candidate_sentences["data"]):
		entity_pairs.append(get_entities(i))
		
	draw_graph(candidate_sentences,entity_pairs,filename,patientid)
	return True
	
# Entities Extraction
def get_entities(sent):
	## chunk 1
	ent1 = ""
	ent2 = ""

	prv_tok_dep = ""		# dependency tag of previous token in the sentence
	prv_tok_text = ""	 # previous token in the sentence

	prefix = ""
	modifier = ""

	#############################################################
	
	for tok in nlp(sent):
		## chunk 2
		# if token is a punctuation mark then move on to the next token
		if tok.dep_ != "punct":
			# check: token is a compound word or not
			if tok.dep_ == "compound":
				prefix = tok.text
				# if the previous word was also a 'compound' then add the current word to it
				if prv_tok_dep == "compound":
					prefix = prv_tok_text + " "+ tok.text
			
			# check: token is a modifier or not
			if tok.dep_.endswith("mod") == True:
				modifier = tok.text
				# if the previous word was also a 'compound' then add the current word to it
				if prv_tok_dep == "compound":
					modifier = prv_tok_text + " "+ tok.text
			
			## chunk 3
			if tok.dep_.find("subj") == True:
				ent1 = modifier +" "+ prefix + " "+ tok.text
				prefix = ""
				modifier = ""
				prv_tok_dep = ""
				prv_tok_text = ""			

			## chunk 4
			if tok.dep_.find("obj") == True:
				ent2 = modifier +" "+ prefix +" "+ tok.text
				
			## chunk 5	
			# update variables
			prv_tok_dep = tok.dep_
			prv_tok_text = tok.text
	#############################################################

	return [ent1.strip(), ent2.strip()]



# Relations Extraction
def get_relation(sent):

	doc = nlp(sent)

	# Matcher class object 
	matcher = Matcher(nlp.vocab)

	#define the pattern 
	pattern = [{'DEP':'ROOT'}, 
						{'DEP':'prep','OP':"?"},
						{'DEP':'agent','OP':"?"},	
						{'POS':'ADJ','OP':"?"}] 

	#matcher.add("matching_1", None, pattern) # Old version
	matcher.add("matching_1", [pattern], on_match=None)	# new version code

	matches = matcher(doc)
	k = len(matches) - 1

	span = doc[matches[k][1]:matches[k][2]] 

	return(span.text)

def draw_graph(candidate_sentences,entity_pairs,filename,patientid):
	relations = [get_relation(i) for i in tqdm(candidate_sentences['data'])]

	# Build Knowledge Graph
	# extract subject
	source = [i[0] for i in entity_pairs]

	# extract object
	target = [i[1] for i in entity_pairs]

	kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})


	# create a directed-graph from a dataframe
	G=nx.from_pandas_edgelist(kg_df, "source", "target",edge_attr=True, create_using=nx.MultiDiGraph())


	# Let’s plot the network
	plt.figure(figsize=(12,12))

	pos = nx.spring_layout(G)
	nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
	plt.savefig('Output/'+patientid+'_graph.png')
	plt.show()

	# Store the source target and relations in csv file
	kg_df.to_csv(filename.split('.')[0]+'_entity.csv')

