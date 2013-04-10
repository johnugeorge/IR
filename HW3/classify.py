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
training_cluster_count=0
training_doc_count=0.0
testing_set_cluster=defaultdict(int)
predicted_set_cluster=defaultdict(int)
predicted_set=defaultdict(list)
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
	#print "Class Prob",class_prob

							       
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
	print testing_doc_count
	print testing_cluster_count


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
	#print resultSet
	print len(resultSet)

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
	print " Final Results match",match
	print "Accuracy ",match/len(testing_set_cluster)

def calculate_micro_F1_values():
	true_positives=0.0
	true_negatives=0.0
	false_positives=0.0
	false_negatives=0.0
	maxSet=defaultdict(float)
	'''
	testing_set_cluster.clear()
	testing_cluster_to_doc_id.clear()
	predicted_set_cluster.clear()
	testing_set_cluster[0]=0
	testing_set_cluster[1]=0
	testing_set_cluster[2]=0
	testing_set_cluster[3]=0
	testing_set_cluster[4]=0
	testing_set_cluster[5]=0
	testing_set_cluster[6]=0
	testing_set_cluster[7]=0
	testing_set_cluster[8]=1
	testing_set_cluster[9]=1
	testing_set_cluster[10]=1
	testing_set_cluster[11]=1
	testing_set_cluster[12]=1
	testing_set_cluster[13]=1
	testing_set_cluster[14]=2
	testing_set_cluster[15]=2
	testing_set_cluster[16]=2
	testing_set_cluster[17]=2
	testing_set_cluster[18]=2
	testing_set_cluster[19]=2
	testing_set_cluster[20]=2
	testing_set_cluster[21]=2
	testing_set_cluster[22]=2
	testing_set_cluster[23]=2
	testing_set_cluster[24]=2
	testing_set_cluster[25]=2
	testing_set_cluster[26]=2
	predicted_set_cluster[0]=0
	predicted_set_cluster[1]=0
	predicted_set_cluster[2]=0
	predicted_set_cluster[3]=0
	predicted_set_cluster[4]=0
	predicted_set_cluster[5]=1
	predicted_set_cluster[6]=1
	predicted_set_cluster[7]=1
	predicted_set_cluster[8]=0
	predicted_set_cluster[9]=0
	predicted_set_cluster[10]=1
	predicted_set_cluster[11]=1
	predicted_set_cluster[12]=1
	predicted_set_cluster[13]=2
	predicted_set_cluster[14]=1
	predicted_set_cluster[15]=1
	predicted_set_cluster[16]=2
	predicted_set_cluster[17]=2
	predicted_set_cluster[18]=2
	predicted_set_cluster[19]=2
	predicted_set_cluster[20]=2
	predicted_set_cluster[21]=2
	predicted_set_cluster[22]=2
	predicted_set_cluster[23]=2
	predicted_set_cluster[24]=2
	predicted_set_cluster[25]=2
	predicted_set_cluster[26]=2

  	testing_cluster_to_doc_id[0]=[0,1,2,3,4,5,6,7]	
  	testing_cluster_to_doc_id[1]=[8,9,10,11,12,13]
  	testing_cluster_to_doc_id[2]=[14,15,16,17,18,19,20,21,22,23,24,25,26]
	'''
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

def getName(cluster):
	if cluster == 0:
		cluster_name="Entertainment"
	elif cluster == 1:
		cluster_name="Business"
	elif cluster == 2:
		cluster_name = "Politics"
	return cluster_name

def printresults():
	print len(predicted_set_cluster)
	for doc in predicted_set_cluster:
		cluster=predicted_set_cluster[doc]
		predicted_set[cluster].append(doc)
	for cluster in predicted_set:
		print
		print "\"",getName(cluster),"\"" , " Size ",len(predicted_set[cluster])
		for doc in predicted_set[cluster]:
			print "\"",getName(testing_set_cluster[doc]).lower(),"\"",doc_to_title[doc] 
			

def main():
	        #'''
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
		#'''
		
		calculate_micro_F1_values()
		printresults()

if __name__ == '__main__':
	main()
