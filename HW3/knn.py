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
k_value=450
query_dict=defaultdict(innerdict)
training_set_cluster=defaultdict(int)
testing_set_cluster=defaultdict(int)
predicted_set_cluster=defaultdict(int)
testing_doc_count=0
training_doc_count=0
testing_cluster_count=0
training_cluster_count=0
match=0.0
testing_set_doc_tokens=defaultdict(list)

def handler(signal, frame):
        print 'You pressed Ctrl+C!..Quiting'
        sys.exit(0)
'''
Module to load Tweets from Json file and add
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
		#print len(tokens_in_title)
		#print len(tokens_in_desc)
		tokens_in_desc.extend(tokens_in_title)
		#print len(tokens_in_desc)
		cluster_to_doc_set[training_cluster_count].add(training_doc_count+1)
		training_set_cluster[training_doc_count+1]=training_cluster_count
		training_doc_count +=1
		add_values_to_dict(tokens_in_desc,training_doc_count)
	training_cluster_count+=1
	print training_doc_count


def create_training_set():
	calculate_idf_value(training_doc_count)
	calculate_tf_idf_value()
	normalize_tf_idf_value()
	#print len(main_dict)
	#print cluster_to_doc_set


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
Module to calculate tf value for each term
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
		testing_set_cluster[testing_doc_count]=testing_cluster_count
		testing_cluster_to_doc_id[testing_cluster_count].append(testing_doc_count)
                calculate_knn(tokens_in_desc,testing_doc_count,testing_cluster_count)
		#break
        testing_cluster_count +=1
        print testing_doc_count
        print testing_cluster_count


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
        #print " Results ",results
	#print " k_nearest ", k_nearest
	count=0
	for elem in k_nearest:
		resultSet[training_set_cluster[elem]]+=k_nearest_similarity[count]
		count+=1
	results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
        #print " Results 1 ",results
        #print " Results ",resultSet
	return results[-1][0]
	#print " k_nearest ", k_nearest

def calculate_knn(tokens,doc_id,actual_cluster_id):
	global match
	global testing_set_doc_tokens
	create_testSet(tokens,doc_id)
	predicted_set_cluster[doc_id]=calculate_nearest_k_neigbours(doc_id)
	#print predicted_set_cluster[doc_id] , actual_cluster_id
	#print "Tokens doc_id",doc_id
	#print testing_set_doc_tokens[doc_id]
        if predicted_set_cluster[doc_id] == actual_cluster_id:
		match += 1

def calculate_tf_value(id_val):
	for token in main_dict[id_val]:
		value=main_dict[id_val][token]
		main_dict[id_val][token]=1+math.log(value,2)

def calculate_micro_F1_values():
	true_positives=0.0
	true_negatives=0.0
	false_positives=0.0
	false_negatives=0.0
	maxSet=defaultdict(float)
	#print testing_set_cluster
	#print
	#print predicted_set_cluster
	print len(testing_set_cluster)
	print len(predicted_set_cluster)
	for cluster in testing_cluster_to_doc_id:
		print "size is",len(testing_cluster_to_doc_id[cluster])," for cluster",cluster
		for doc in testing_set_cluster:
			actual=testing_set_cluster[doc]
			predicted=predicted_set_cluster[doc]
			#print "actual ",actual,"predicted ",predicted," for doc ",doc
			if cluster == actual and predicted == cluster:
				#print "true_positive"
				true_positives += 1
			elif cluster != actual and predicted == cluster:
				#print "false_positive"
				false_positives += 1
			elif cluster == actual and predicted != cluster:
				#print "false_negative"
				false_negatives += 1
			elif cluster != actual and predicted != cluster:
				#print "true_negative"
				true_negatives += 1
	print "true_postives",true_positives
	print "true_negatives",true_negatives
	print "false_postives",false_positives
	print "false_negatives",false_negatives
	recall=true_positives/(true_positives + false_negatives)
	precision=true_positives/(true_positives + false_positives)
	f1_values=2*recall*precision/(recall+precision)
	print f1_values
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
        print "Loading Test Set from Local file"
        print
        fileloc="test_entertainment.json"
        loadTestset(fileloc)
        fileloc="test_business.json"
        loadTestset(fileloc)
        fileloc="test_politics.json"
        loadTestset(fileloc)
	print " Match", match/(testing_doc_count)
	calculate_micro_F1_values()

if __name__ == '__main__':
	main()
