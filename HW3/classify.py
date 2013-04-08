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
resultSet=defaultdict(innerdict)
class_prob=defaultdict(float)
training_cluster_count=0
training_doc_count=0.0
testing_set_cluster=defaultdict(int)
testing_cluster_count=0
testing_doc_count=0.0
set_of_tokens=set()
total_vocab_tokens=0


def handler(signal, frame):
        print 'You pressed Ctrl+C!..Quiting'
        sys.exit(0)
'''
Module to load Tweets from Json file and add
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
		#print len(tokens_in_title)
		#print len(tokens_in_desc)
		tokens_in_desc.extend(tokens_in_title)
		#print len(tokens_in_desc)
		training_doc_count +=1
		add_values_to_dict(tokens_in_desc,training_doc_count,training_cluster_count)
	training_cluster_count +=1
	print training_doc_count
	print training_cluster_count
	print "Total Vocabulary",len(set_of_tokens)
	total_vocab_tokens=len(set_of_tokens)
	calculate_class_prob()
	print "Class Prob",class_prob

							       
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
		create_testing_set(tokens_in_desc,testing_doc_count,testing_cluster_count)
	testing_cluster_count +=1
	print testing_doc_count
	print testing_cluster_count


def calculate_class_prob():
	for cluster in cluster_set:
		total_docs_in_cluster=len(cluster_set_to_doc_id[cluster])
		class_prob[cluster]=total_docs_in_cluster/training_doc_count
	

def create_testing_set(tokens,doc_id,cluster_id):
	testing_set_cluster[doc_id]=cluster_id
	for token in tokens:
		token=token.lower()
		testing_dict[doc_id][token]+=1

'''
Module to add term in Main dictionary and Document Frequency table
'''

def add_values_to_dict(tokens,doc_id,cluster_id):
	cluster_set[cluster_id].extend(tokens)
	cluster_set_to_doc_id[cluster_id].append(doc_id)
	#doc_id_to_tokens[doc_id]=tokens
	for token in tokens:
		token=token.lower()
		main_dict[cluster_id][token]+=1
		set_of_tokens.add(token)
	return

def calculate_token_prob(token,cluster_id):
	total_token_occurence=0.0
	total_words=0.0
	total_token_occurence = main_dict[cluster_id][token]
	total_words= len(cluster_set[cluster_id])
	prob_per_cluster=(total_token_occurence+1)/(total_words+total_vocab_tokens)
	return prob_per_cluster

def log_val(val):
	return math.log(val,2)

def calculate_naive_classifier():
	for doc in testing_dict:
		for cluster in cluster_set:
			resultSet[doc][cluster] += log_val(class_prob[cluster])
			for token in testing_dict[doc]:
				val=calculate_token_prob(token,cluster)
				resultSet[doc][cluster] += log_val(val)
	print resultSet
	print len(resultSet)

def calculate_accuracy():
	match=0.0
	maxSet=defaultdict(float)
	for doc in resultSet:
		for cluster in resultSet[doc]:
			maxSet[cluster]=resultSet[doc][cluster]
		results=[(key,val) for key, val in sorted(maxSet.iteritems(), key=lambda (k,v): (v,k))]
		cluster_id=results[-1][0]
		if testing_set_cluster[doc] == cluster_id:
			match+=1
	print " Final Results match",match
	print "Accuracy ",match/len(testing_set_cluster)

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
	        print "Loading Test Set from Local file"
		print
		fileloc="test_entertainment.json"
		loadTestset(fileloc)
		fileloc="test_business.json"
		loadTestset(fileloc)
		fileloc="test_politics.json"
		loadTestset(fileloc)
		calculate_naive_classifier()
		calculate_accuracy()

if __name__ == '__main__':
	main()
