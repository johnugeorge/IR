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
resultSet=defaultdict(float)
k_value=2


def handler(signal, frame):
        print 'You pressed Ctrl+C!..Quiting'
        sys.exit(0)
'''
Module to load Tweets from Json file and add
in Datastructures
'''

def loadQueries(fileloc):
        data=[]
	total_doc_count=0
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
		total_doc_count +=1
		add_values_to_dict(tokens_in_desc,total_doc_count)
	print total_doc_count
	calculate_idf_value(total_doc_count)
	calculate_tf_idf_value()
	normalize_tf_idf_value()
	print main_dict
	ececute_k_means(total_doc_count)


'''
K-Means Algorithm
'''

def ececute_k_means(total_doc_count):
	root_nodes=create_random_root_nodes(total_doc_count)
	for doc in main_dict:
		calculate_nearest_node(doc,root_nodes)
	print cluster_set

#def print_tables(cluster_set):


def calculate_nearest_node(doc,root_nodes):
		global resultSet
		resultSet=defaultdict(float)
		for root_doc in root_nodes:
			value=0
			for token in main_dict[root_doc]:
				if token in main_dict[doc]:
					value=value+main_dict[root_doc][token]*main_dict[doc][token]
			if value > 0:
				resultSet[root_doc]=value
		results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
		print "-----results----", doc,root_nodes
 		print results
		print "set ",cluster_set
		if results:
			nearest_root_node=results[-1][0]
		else:
			print " adding node",root_nodes[0]
			nearest_root_node=root_nodes[0]
		cluster_set[nearest_root_node][1].add(doc)
		print cluster_set
		print "-----results end----"

def create_random_root_nodes(total_doc_count):
	root_nodes=[]
	init_array=[1,3]
	count=0
	while len(root_nodes) != k_value:
		rand_val=random.randint(1, total_doc_count)
		rand_val=init_array[count]
		count+=1
		if rand_val not in root_nodes:
			root_nodes.append(rand_val)
			cluster_set[rand_val] = []
			cluster_set[rand_val].append(0) #for centroid value
			cluster_set[rand_val].append(set()) # for set of nodes
	print root_nodes
	return root_nodes


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

def calculate_tf_value(id_val):
		for token in main_dict[id_val]:
			value=main_dict[id_val][token]
			main_dict[id_val][token]=1+math.log(value,2)


def main():
	        print "Loading Queries from Local file"
		print
	        signal.signal(signal.SIGINT, handler)
		fileloc="test.json"
		loadQueries(fileloc)

if __name__ == '__main__':
	main()
