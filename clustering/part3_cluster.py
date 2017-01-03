import re
import signal
import sys
import json
import math
import bisect
import random
from random import randrange
from collections import defaultdict

def innerdict():
	        return defaultdict(float)

main_dict=defaultdict(innerdict)
document_freq_dict=defaultdict(float)
doc_id_to_tokens=defaultdict(list)
cluster_set=defaultdict(list)
resultSet=defaultdict(float)
cluster_to_doc_set=defaultdict(set)
doc_id_title=defaultdict(str)
#k_value=10
search_results=30

def handler(signal, frame):
        print 'You pressed Ctrl+C!..Quiting'
        sys.exit(0)
'''
Module to load Queries from Json file and add
in Datastructures
'''

def loadQueries(fileloc):
        data=[]
	global search_results
	total_doc_count=0
        json_data=open(fileloc,'r')
        buf=json_data.readlines()
        json_data.close()
        for line in buf:
                data=json.loads(line)
		tokens_in_title=re.findall(r"[\w]+", data['Title'],re.UNICODE)
		tokens_in_desc=re.findall(r"[\w]+", data['Description'],re.UNICODE)
		tokens_in_desc.extend(tokens_in_title)
		cluster_id=total_doc_count/search_results
		cluster_to_doc_set[cluster_id].add(total_doc_count+1)
		total_doc_count +=1
		doc_id_title[total_doc_count]=data['Title']
		add_values_to_dict(tokens_in_desc,total_doc_count)
	calculate_idf_value(total_doc_count)
	calculate_tf_idf_value()
	normalize_tf_idf_value()
	return total_doc_count


'''
K-Means Algorithm
'''

def execute_k_means(root_nodes,total_doc_count,k_value):
	for doc in main_dict:
		calculate_nearest_node(doc,root_nodes)
	calculate_centroid()
	#print cluster_set
	initial_rss=calculate_rss()
	ret = call_iterations(initial_rss)
	return ret

'''
Function to repeat iterations until the RSS values remain same
'''
def call_iterations(rss_value):
	prev_rss_val=rss_value
	count=1
	while True:
		for elem in cluster_set:
			cluster_set[elem][1].clear()
		for doc in main_dict:
			recalculate_cluster_nodes(doc)
		calculate_centroid()
		present_rss_val=calculate_rss()
		if present_rss_val == prev_rss_val:
			for elem in cluster_set:
				if len(cluster_set[elem][1]) == 0:
					return -1
			return present_rss_val
		prev_rss_val = present_rss_val
		count +=1

'''
Function to calculate rss for cluster obtained
'''
def calculate_rss():
	rss_val=0
	for elem in cluster_set:
		centroid_tokens=cluster_set[elem][0].keys()
		for node in cluster_set[elem][1]:
			doc_tokens=main_dict[node].keys()
			doc_tokens.extend(centroid_tokens)
			set_of_tokens=set(doc_tokens)
			for token in set_of_tokens:
				diff_val = main_dict[node][token] - cluster_set[elem][0][token]
				rss_val += diff_val*diff_val
	return rss_val


'''
Function to asssign a cluster for a particular point
'''
def recalculate_cluster_nodes(doc):
		global resultSet
		resultSet=defaultdict(float)
		for cluster in cluster_set:
			value=0
			for token in main_dict[doc]:
				if token in cluster_set[cluster][0]:
					value=value+main_dict[doc][token]*cluster_set[cluster][0][token]
			if value > 0:
				resultSet[cluster]=value
		results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
		if results:
			nearest_root_node=results[-1][0]
		else:
			nearest_root_node=0
		cluster_set[nearest_root_node][1].add(doc)

'''
Function to calculate centroid of a cluster
'''
def calculate_centroid():
	for root_doc in cluster_set:
		set_of_member_set=cluster_set[root_doc][1]
		total_members=len(set_of_member_set)
		cluster_centroid_vector=cluster_set[root_doc][0]
		cluster_centroid_vector.clear()
		for elem in set_of_member_set:
			for term in main_dict[elem]:
				cluster_centroid_vector[term] += main_dict[elem][term]
		for term in cluster_centroid_vector:
			cluster_centroid_vector[term]= cluster_centroid_vector[term]/total_members
		cluster_set[root_doc][0]=cluster_centroid_vector

'''
Function to get the nearest centroid for a particular points
'''
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
		if results:
			nearest_root_node=results[-1][0]
		else:
			nearest_root_node=root_nodes[0]
		cluster_set[root_nodes.index(nearest_root_node)][1].add(doc)

'''
Function to create random seed nodes based on value of K_Value chosen and total points
'''
def create_random_root_nodes(total_doc_count,k_value):
	root_nodes=[]
	cluster_set.clear()
	while len(root_nodes) != k_value:
		rand_val=random.randint(1, total_doc_count)
		if rand_val not in root_nodes:
			root_nodes.append(rand_val)
			cluster_set[root_nodes.index(rand_val)] = []
			cluster_set[root_nodes.index(rand_val)].append(defaultdict(float)) #for centroid value
			cluster_set[root_nodes.index(rand_val)].append(set()) # for set of nodes
	print " Inital root nodes list",root_nodes
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

'''
Function to calculate purity value of obtained cluster
'''
def calculate_purity():
	total_max_value = 0.0
	for cluster in cluster_set:
		calculated_results=cluster_set[cluster][1]
		maxValue=0
		for elem in cluster_to_doc_set:
			common_set=calculated_results & cluster_to_doc_set[elem]
			if maxValue < len(common_set):
				maxValue=len(common_set)
		total_max_value += maxValue
	purity_value=total_max_value/len(main_dict)
	return purity_value
	
'''
Main Function
'''
def main():
	        print "Loading Queries from Local file"
		print
		global search_results
		new_root_node=[]
	        signal.signal(signal.SIGINT, handler)
		fileloc="cluster.json"
		doc_count=loadQueries(fileloc)
		k_value=10
		root_nodes=create_random_root_nodes(doc_count,k_value)
		ret = execute_k_means(root_nodes,doc_count,k_value)
		while ret == -1:
			root_nodes=create_random_root_nodes(doc_count,k_value)
			ret = execute_k_means(root_nodes,doc_count,k_value)
		purity=calculate_purity()
		
		print "Initial Purity Value is ",purity, " RSS Value is ",ret
		print
		for elem in cluster_set:
			val=random.sample(cluster_set[elem][1],1)[0]
			new_root_node.append(val)
		print "New root nodes list ",new_root_node
		ret = execute_k_means(new_root_node,doc_count,k_value)
		while ret == -1:
			new_root_node.clear()
			root_nodes=create_random_root_nodes(doc_count,k_value)
			ret = execute_k_means(root_nodes,doc_count,k_value)
			for elem in cluster_set:
				val=random.sample(cluster_set[elem][1],1)[0]
				new_root_node.append(val)
			print "New root node ",new_root_node
			ret = execute_k_means(new_root_node,doc_count,k_value)
		purity=calculate_purity()
		iter_val=1
		for elem in cluster_set:
			print
			print "Cluster ",iter_val
			print 
			for doc in cluster_set[elem][1]:
				cluster_id=doc/search_results
				if cluster_id == 0:
					print "texas aggies" ,":",doc_id_title[doc]
				elif cluster_id == 1:
					print "texas longhorns" ,":",doc_id_title[doc]
				elif cluster_id == 2:
					print "duke blue devils" ,":",doc_id_title[doc]
				elif cluster_id == 3:
					print "dallas cowboys" ,":",doc_id_title[doc]
				elif cluster_id == 4:
					print "dallas mavericks" ,":",doc_id_title[doc]
			iter_val+=1
		print
		print "New Purity Value is ",purity, " RSS Value is ",ret
		print
		


if __name__ == '__main__':
	main()
