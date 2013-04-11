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
document_freq_dict=defaultdict(float)
doc_id_to_tokens=defaultdict(list)
cluster_set=defaultdict(list)
testing_cluster_to_doc_id=defaultdict(list)
resultSet=defaultdict(float)
cluster_to_doc_set=defaultdict(set)
query_dict=defaultdict(innerdict)
training_set_cluster=defaultdict(int)
testing_set_cluster=defaultdict(int)
predicted_set_cluster=defaultdict(int)
testing_set_doc_tokens=defaultdict(list)
predicted_set=defaultdict(list)
doc_to_title=defaultdict(str)

testing_doc_count=0
training_doc_count=0
testing_cluster_count=0
training_cluster_count=0
match=0.0
k_value=450

def handler(signal, frame):
        print 'You pressed Ctrl+C!..Quiting'
        sys.exit(0)

'''
Module to load Training data from Json file and add
in Datastructures
'''

def loadQueries(fileloc):
        data=[]
	global training_doc_count
	global training_cluster_count
        json_data=open(fileloc,'r')
        buf=json_data.readlines()
        json_data.close()
        for line in buf:
                data=json.loads(line)
		tokens_in_title=re.findall(r"[\w]+", data['Title'],re.UNICODE)
		tokens_in_desc=re.findall(r"[\w]+", data['Description'],re.UNICODE)
		tokens_in_desc.extend(tokens_in_title)
		cluster_to_doc_set[training_cluster_count].add(training_doc_count+1)
		training_set_cluster[training_doc_count+1]=training_cluster_count
		training_doc_count +=1
		add_values_to_dict(tokens_in_desc,training_doc_count)
	training_cluster_count+=1


def create_training_set():
	calculate_idf_value(training_doc_count)
	calculate_tf_idf_value()
	normalize_tf_idf_value()


'''
Module to normalize tf-idf values
'''

def normalize_tf_idf_value():
		global main_dict
		for doc in main_dict:
			square=0
			for term in main_dict[doc]:
				square=square+ main_dict[doc][term]* main_dict[doc][term]
			if square == 0:
				continue
			sq_root=math.sqrt(square)
			for term in main_dict[doc]:
				value= main_dict[doc][term]
				main_dict[doc][term]=value/sq_root


'''
Module to calculate tf-idf value for each term
'''

def calculate_tf_idf_value():
	for doc in main_dict:
		for term in main_dict[doc]:
			value= main_dict[doc][term]
			main_dict[doc][term]=value*document_freq_dict[term]


'''
Module to calculate idf value for each term
'''

def calculate_idf_value(total_docs):
	for token in document_freq_dict:
		value=document_freq_dict[token]
		document_freq_dict[token]=math.log(total_docs/value,2)
							       

'''
Module to add term in Main dictionary and Document Frequency table
'''

def add_values_to_dict(tokens,id_val):
	set_of_tokens= set()
	for token in tokens:
		token=token.lower()
		main_dict[id_val][token]+=1
		set_of_tokens.add(token)
	for elem in set_of_tokens:
		elem=elem.lower()
		document_freq_dict[elem]+=1
	calculate_tf_value(id_val)
	return

'''
Module to calculate tf-idf value for each term of a particular testing doc
'''
def create_testSet(tokens,doc_id):
	global query_dict
	query_dict=defaultdict(innerdict)
	square=0
	for token in tokens:
		token=token.lower()
		query_dict[doc_id][token]+=1
	for token in query_dict[doc_id]:
	        token=token.lower()
	        value=query_dict[doc_id][token]
	        value=1+math.log(value,2)
		if token in document_freq_dict:
	         	query_dict[doc_id][token]=value*document_freq_dict[token]
		square+=query_dict[doc_id][token] * query_dict[doc_id][token]	
        if square==0:
		return 2
        sq_root=math.sqrt(square)
        for token in query_dict[doc_id]:
		token=token.lower()
	        value= query_dict[doc_id][token]
	        query_dict[doc_id][token]=value/sq_root
	return 1

'''
Module to load testing set from Json file and add
in Datastructures
'''

def loadTestset(fileloc):
        global testing_doc_count
        global testing_cluster_count
	global testing_set_doc_tokens
        data=[]
        json_data=open(fileloc,'r')
        buf=json_data.readlines()
        json_data.close()
        for line in buf:
                data=json.loads(line)
                tokens_in_title=re.findall(r"[\w]+", data['Title'],re.UNICODE)
                tokens_in_desc=re.findall(r"[\w]+", data['Description'],re.UNICODE)
                tokens_in_desc.extend(tokens_in_title)
                testing_doc_count += 1
		testing_set_doc_tokens[testing_doc_count]=tokens_in_desc
		doc_to_title[testing_doc_count]=data['Title']
		testing_set_cluster[testing_doc_count]=testing_cluster_count
		testing_cluster_to_doc_id[testing_cluster_count].append(testing_doc_count)
                calculate_knn(tokens_in_desc,testing_doc_count,testing_cluster_count)
        testing_cluster_count +=1

'''
Module to calculate the k nearest neigbours for a particular doc
'''

def calculate_nearest_k_neigbours(doc_id):
	global resultSet
	resultSet=defaultdict(float)
	for doc in main_dict:
		value=0
		for token in query_dict[doc_id]:
			if token in main_dict[doc]:
				value=value+query_dict[doc_id][token]*main_dict[doc][token]
		if value > 0:
			resultSet[doc]=value
	results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
	k_nearest=[elem[0] for elem in results][-k_value:]
	k_nearest_similarity=[elem[1] for elem in results][-k_value:]
	resultSet=defaultdict(float)
	count=0
	for elem in k_nearest:
		resultSet[training_set_cluster[elem]]+=k_nearest_similarity[count]
		count+=1
	results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
	return results[-1][0]

'''
K-NN Algorithm
'''
def calculate_knn(tokens,doc_id,actual_cluster_id):
	global match
	global testing_set_doc_tokens
	create_testSet(tokens,doc_id)
	predicted_set_cluster[doc_id]=calculate_nearest_k_neigbours(doc_id)
        if predicted_set_cluster[doc_id] == actual_cluster_id:
		match += 1

'''
Module to calculate tf value for each term
'''

def calculate_tf_value(id_val):
	for token in main_dict[id_val]:
		value=main_dict[id_val][token]
		main_dict[id_val][token]=1+math.log(value,2)

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
	create_training_set()
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
	f1_value=calculate_micro_F1_values()
	printresults()
	print
	print " F1 Value of Classified output",f1_value
	print

if __name__ == '__main__':
	main()
