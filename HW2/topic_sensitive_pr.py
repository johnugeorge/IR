import re
import signal
import sys
import json
import math
import bisect
from numpy import *
from collections import defaultdict

userCount=-1
alpha_factor=0.1
prec=0.0001
user_id_to_logical_no=defaultdict(int)
logical_no_to_user_id=defaultdict(int)
logical_to_logical=defaultdict(int)
reverse_logical_to_logical=defaultdict(int)
user_id_to_screen_name=defaultdict(str)
incoming_graph=defaultdict(set)
incoming_graph_updated=defaultdict(set)
outgoing_graph=defaultdict(set)
outgoing_graph_updated=defaultdict(set)
resultSet=defaultdict(float)
label_id_dict=defaultdict(list)

topics={1:'ARTS',2:'BUSINESS',3:'COMPUTERS',4:'GAMES',5:'HEALTH',6:'HOME',7:'KIDS AND TEENS',8:'NEWS',9:'RECREATION',10:'REFERENCE',11:'REGIONAL',12:'SCIENCE',13:'SHOPPING',14:'SOCIETY',15:'SPORTS',16:'WORLD'}
maxTopics=16
def innerdict():
        return defaultdict(float)
'''
Module to load Tweets from Json file and add
in Datastructures
'''

def loadTweets(fileloc):
        data=[]
        count=1
        json_data=open(fileloc,'r')
        buf=json_data.readlines()
        json_data.close()
        for line in buf:
                data=json.loads(line)
                tokens=re.findall(r"[\w]+", data['text'],re.UNICODE)
		process_data(data)
	assign_labels()

'''
Module to Calculate PageRank from
incoming links of valid users
'''
def calculate_pagerank(label_id):
	global resultSet
	resultSet=defaultdict(float)
	total_users=len(logical_to_logical)
	pagerank_list=[1.0 if  logical_to_logical[elem] in label_id_dict[label_id] else 0 for elem in logical_to_logical]	
	value=0
	iteration=1
	new_pagerank_list=pagerank_list[:]
	user_list=pagerank_list[:]
	total_users_per_label=len( label_id_dict[label_id])
	if not total_users_per_label:
		return
	while 1:
		count=0
		for user in pagerank_list:
			if count in incoming_graph_updated:
				for elem in incoming_graph_updated[count]:
					total_outgoing_links=len(outgoing_graph_updated[elem])
					prev_pr=pagerank_list[elem]
					value=value+prev_pr/total_outgoing_links
			if not user_list[int(user)]:
				new_pagerank_list[count]=(1- alpha_factor)*value
			else:
				new_pagerank_list[count]=alpha_factor/float(total_users_per_label) + (1- alpha_factor)*value
			value=0
			count+=1
		diff=[x-y for x,y in zip(new_pagerank_list,pagerank_list)]
		if all([math.fabs(item) <= prec for item in diff]):
			iter_val=0
			for val in new_pagerank_list:
				resultSet[iter_val]=new_pagerank_list[iter_val]
				iter_val+=1
			results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
			return results
		pagerank_list=new_pagerank_list[:]
		iteration+=1
		
'''
Module to assign labels to users.
Assign labels based on total incoming links.
Hence, mentioned users can be clustered
and best results can be provided
'''			
def assign_labels():
         results=[(key,val) for key, val in sorted(incoming_graph.iteritems(), key=lambda (k,v): (len(v),k))]
         count=1
         for elem in reversed(results):
                label_id_dict[count].extend(list(elem[1]))
                count+=1
                if count > maxTopics:
                        break
	 count=0
	 for elem in incoming_graph:
		logical_to_logical[count]=elem
		reverse_logical_to_logical[elem]=count
		count+=1
	 for elem in incoming_graph:
		for user in incoming_graph[elem]:
			incoming_graph_updated[reverse_logical_to_logical[elem]].add(reverse_logical_to_logical[user])
	 for elem in outgoing_graph:
		for user in outgoing_graph[elem]:
			outgoing_graph_updated[reverse_logical_to_logical[elem]].add(reverse_logical_to_logical[user])
	
'''
Module to print Final Results
'''
	
def printResult(label_id,results, no_of_results):
	count=1
	if len(label_id_dict[label_id]) == 0:
		return
	print "============ Results for",topics[label_id],"==============="
	for user in reversed(results):
		if user[0] not in incoming_graph:
			continue
		user_id=logical_no_to_user_id[logical_to_logical[user[0]]]
		print "Rank: ",count , " Rank Value ",user[1]
		print "User Id: ",user_id
		print "Screen Name: ",user_id_to_screen_name[user_id]
		print
		if count== no_of_results:
			break
		count+=1
	
'''
Module which maps logical id to user_id's,
user_id's to screen names
'''


def process_data(data):
	global userCount
	main_id=0
	user_id=data['user']['id']
	if user_id not in user_id_to_logical_no:
		userCount+=1
		user_id_to_logical_no[user_id] = userCount
		logical_no_to_user_id[userCount]=user_id
		user_id_to_screen_name[user_id]= data['user']['screen_name']
		main_id=userCount;
	else:
		main_id= user_id_to_logical_no[user_id]
	for user in data['entities']['user_mentions']:
		mention_id=user['id']
		if mention_id not in user_id_to_logical_no:
			userCount+=1
                	user_id_to_logical_no[mention_id] = userCount
			logical_no_to_user_id[userCount]=mention_id
			user_id_to_screen_name[mention_id]= user['screen_name']
			create_links(main_id,userCount)
		else:	
			mention_id_val=user_id_to_logical_no[mention_id]
			create_links(main_id,mention_id_val)

'''
Module to create incoming and outgoing graphs per user
'''

def create_links(parent_id,mention_id):
	if parent_id==mention_id:
		return
	outgoing_graph[parent_id].add(mention_id)
	if parent_id not in incoming_graph:
		incoming_graph[parent_id]=set()
	incoming_graph[mention_id].add(parent_id)
	if mention_id not in outgoing_graph:
		outgoing_graph[mention_id]=set()


def main():
        print "Loading Tweets from Json File"
	print
        fileloc="mars_tweets_medium.json"
        loadTweets(fileloc)
	label_id=1
	while label_id <= maxTopics:
        	results=calculate_pagerank(label_id)
		printResult(label_id,results,10)
		label_id+=1
        print "done"


if __name__ == '__main__':
        main()


