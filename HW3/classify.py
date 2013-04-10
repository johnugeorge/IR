import re
import signal
import sys
import json
import math
import bisect
import random
from collections import defaultdict


def innerdict():
        return defaultdict(float)

main_dict=defaultdict(innerdict)
testing_dict=defaultdict(innerdict)
doc_id_to_tokens=defaultdict(list)
cluster_set=defaultdict(list)
cluster_set_to_doc_id=defaultdict(list)
doc_to_title=defaultdict(str)
testing_cluster_to_doc_id=defaultdict(list)
resultSet=defaultdict(innerdict)
class_prob=defaultdict(float)
testing_set_cluster=defaultdict(int)
predicted_set_cluster=defaultdict(int)
predicted_set=defaultdict(list)
set_of_tokens=set()

training_doc_count=0.0
testing_cluster_count=0
training_cluster_count=0
testing_doc_count=0.0
total_vocab_tokens=0


def handler(signal, frame):
        print 'You pressed Ctrl+C!..Quiting'
        sys.exit(0)
'''
Module to load training set from Json file and add
in Datastructures
'''

def loadQueries(fileloc):
	global training_doc_count
	global training_cluster_count
	global total_vocab_tokens
        data=[]
        json_data=open(fileloc,'r')
        buf=json_data.readlines()
        json_data.close()
        for line in buf:
                data=json.loads(line)
		tokens_in_title=re.findall(r"[\w]+", data['Title'],re.UNICODE)
		tokens_in_desc=re.findall(r"[\w]+", data['Description'],re.UNICODE)
		tokens_in_desc.extend(tokens_in_title)
		training_doc_count +=1
		add_values_to_dict(tokens_in_desc,training_doc_count,training_cluster_count)
	training_cluster_count +=1
	total_vocab_tokens=len(set_of_tokens)
	calculate_class_prob()

							       
'''
Module to load testing set from Json file and add
in Datastructures
'''

def loadTestset(fileloc):
	global testing_doc_count
        global testing_cluster_count
	data=[]
        total_test_set=0
	json_data=open(fileloc,'r')
        buf=json_data.readlines()
        json_data.close()
        for line in buf:
                data=json.loads(line)
		tokens_in_title=re.findall(r"[\w]+", data['Title'],re.UNICODE)
		tokens_in_desc=re.findall(r"[\w]+", data['Description'],re.UNICODE)
		tokens_in_desc.extend(tokens_in_title)
		testing_doc_count += 1
		doc_to_title[testing_doc_count]=data['Title']
		create_testing_set(tokens_in_desc,testing_doc_count,testing_cluster_count)
	testing_cluster_count +=1

'''
Module to calculate static probability of a class
'''
def calculate_class_prob():
	for cluster in cluster_set:
		total_docs_in_cluster=len(cluster_set_to_doc_id[cluster])
		class_prob[cluster]=total_docs_in_cluster/training_doc_count
	

def create_testing_set(tokens,doc_id,cluster_id):
	testing_set_cluster[doc_id]=cluster_id
	testing_cluster_to_doc_id[cluster_id].append(doc_id)
	for token in tokens:
		token=token.lower()
		testing_dict[doc_id][token]+=1

'''
Module to add term in Main dictionary and Document Frequency table
'''

def add_values_to_dict(tokens,doc_id,cluster_id):
	cluster_set[cluster_id].extend(tokens)
	cluster_set_to_doc_id[cluster_id].append(doc_id)
	for token in tokens:
		token=token.lower()
		main_dict[cluster_id][token]+=1
		set_of_tokens.add(token)
	return

'''
Module to calculate the term probability for a particular category
'''
def calculate_token_prob(token,cluster_id):
	total_token_occurence=0.0
	total_words=0.0
	total_token_occurence = main_dict[cluster_id][token]
	total_words= len(cluster_set[cluster_id])
	prob_per_cluster=(total_token_occurence+1)/(total_words+total_vocab_tokens)
	return prob_per_cluster

'''
Returns the log value of the input
'''
def log_val(val):
	return math.log(val,2)

'''
Implementation of Naive Bayes Classifier
'''
def calculate_naive_classifier():
	for doc in testing_dict:
		for cluster in cluster_set:
			resultSet[doc][cluster] += log_val(class_prob[cluster])
			for token in testing_dict[doc]:
				val=calculate_token_prob(token,cluster)
				resultSet[doc][cluster] += log_val(val)
'''
Module to calculate accuracy of the classifier. 
'''
def calculate_accuracy():
	match=0.0
	maxSet=defaultdict(float)
	for doc in resultSet:
		for cluster in resultSet[doc]:
			maxSet[cluster]=resultSet[doc][cluster]
		results=[(key,val) for key, val in sorted(maxSet.iteritems(), key=lambda (k,v): (v,k))]
		cluster_id=results[-1][0]
		predicted_set_cluster[doc]=cluster_id;
		if testing_set_cluster[doc] == cluster_id:
			match +=1
'''
Module to calculate the F1 value for the classfied results
'''
def calculate_micro_F1_values():
	true_positives=0.0
	true_negatives=0.0
	false_positives=0.0
	false_negatives=0.0
	maxSet=defaultdict(float)
	
	for cluster in testing_cluster_to_doc_id:
		for doc in testing_set_cluster:
			actual=testing_set_cluster[doc]
			predicted=predicted_set_cluster[doc]
			if cluster == actual and predicted == cluster:
				true_positives += 1
			elif cluster != actual and predicted == cluster:
				false_positives += 1
			elif cluster == actual and predicted != cluster:
				false_negatives += 1
			elif cluster != actual and predicted != cluster:
				true_negatives += 1

	recall=true_positives/(true_positives + false_negatives)
	precision=true_positives/(true_positives + false_positives)
	f1_values=2*recall*precision/(recall+precision)
	return f1_values

'''
Function that returns the name of the category based on cluster id
'''
def getName(cluster):
	if cluster == 0:
		cluster_name="Entertainment"
	elif cluster == 1:
		cluster_name="Business"
	elif cluster == 2:
		cluster_name = "Politics"
	return cluster_name

'''
Module to print the results in the desired format
'''
def printresults():
	for doc in predicted_set_cluster:
		cluster=predicted_set_cluster[doc]
		predicted_set[cluster].append(doc)
	for cluster in predicted_set:
		print
		print getName(cluster)
		print
		for doc in predicted_set[cluster]:
			print getName(testing_set_cluster[doc]).lower(),":",doc_to_title[doc] 
			
'''
Main Function
'''
def main():
		print "Loading Training Set from Local file"
		print
	        signal.signal(signal.SIGINT, handler)
		fileloc="entertainment.json"
		loadQueries(fileloc)
		fileloc="business.json"
		loadQueries(fileloc)
		fileloc="politics.json"
		loadQueries(fileloc)
		print  "Training Doc Count:",training_doc_count
		print
	        print "Loading Test Set from Local file"
		print
		fileloc="test_entertainment.json"
		loadTestset(fileloc)
		fileloc="test_business.json"
		loadTestset(fileloc)
		fileloc="test_politics.json"
		loadTestset(fileloc)
		print "Testing Doc count:",testing_doc_count
		calculate_naive_classifier()
		calculate_accuracy()
		
		f1_value= calculate_micro_F1_values()
		printresults()
		print
		print "F1 Value:",f1_value
		print

if __name__ == '__main__':
	main()
