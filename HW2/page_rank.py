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
prec=0.00001
user_id_to_logical_no=defaultdict(int)
logical_no_to_user_id=defaultdict(int)
user_id_to_screen_name=defaultdict(str)
incoming_graph=defaultdict(set)
outgoing_graph=defaultdict(set)
resultSet=defaultdict(float)

def innerdict():
        return defaultdict(float)

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
                #id_val=data['id']
                #if count == 5:
                #       break
                #count+=1
	#print  user_id_to_logical_no
	#print
	#print user_id_to_screen_name	
	#print
	#print outgoing_graph
	#print
	#print incoming_graph
	print len(user_id_to_screen_name)
	print len(outgoing_graph)
	print len(incoming_graph)


def calculate_pagerank():
	total_users=len(user_id_to_logical_no)
	pagerank_list=[1]* total_users
	#pagerank_list=ones(total_users)
	value=0
	iteration=1
	#new_pagerank_list=pagerank_list.copy()
	new_pagerank_list=pagerank_list[:]
	#print " New PageRank ",new_pagerank_list
	while 1:
		count=0
		for user in pagerank_list:
			if count in incoming_graph:
				for elem in incoming_graph[count]:
					total_outgoing_links=len(outgoing_graph[elem])
					prev_pr=pagerank_list[elem]
					value=value+prev_pr/total_outgoing_links
					#print "Value ",value
			new_pagerank_list[count]=alpha_factor + (1- alpha_factor)*value
			value=0
		#	print " In loop  PageRank ",new_pagerank_list ," count ",count
			
			count+=1
		#diff=new_pagerank_list-pagerank_list
		diff=[x-y for x,y in zip(new_pagerank_list,pagerank_list)]
		#print "Iterations needed ",iteration
		if all([math.fabs(item) <= prec for item in diff]):
			print "Iterations needed ",iteration
			iter_val=0
			for val in new_pagerank_list:
				resultSet[iter_val]=new_pagerank_list[iter_val]
				iter_val+=1
			results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
			#print results[-20:]
			return results
		#if(((abs(diff)) <= prec).all()):
		#	break
		#pagerank_list=new_pagerank_list.copy()
		pagerank_list=new_pagerank_list[:]
		iteration+=1
		
					
def printResult(results, no_of_results):
	count=1
	for user in reversed(results):
		if user[0] not in incoming_graph:
			continue
		user_id=logical_no_to_user_id[user[0]]
		print "Rank: ",count
		print "User Id: ",user_id
		print "Screen Name: ",user_id_to_screen_name[user_id]
		print
		if count== no_of_results:
			break
		count+=1
	

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
		#print "User Id ",userCount , " Tweet user id ",user_id, " Screen name ",user_id_to_screen_name[user_id]
	for user in data['entities']['user_mentions']:
		#userCount+=1
		mention_id=user['id']
		#create_links(main_id,userCount)
		if mention_id not in user_id_to_logical_no:
			#print "User Id ",userCount , " Tweet user id ",mention_id, " Screen name ",user['screen_name']
			userCount+=1
                	user_id_to_logical_no[mention_id] = userCount
			logical_no_to_user_id[userCount]=mention_id
			user_id_to_screen_name[mention_id]= user['screen_name']
			create_links(main_id,userCount)
		else:	
			mention_id_val=user_id_to_logical_no[mention_id]
			create_links(main_id,mention_id_val)

def create_links(parent_id,mention_id):
	if parent_id==mention_id:
		return
	outgoing_graph[parent_id].add(mention_id)
	if parent_id not in incoming_graph:
		incoming_graph[parent_id]=set()
	incoming_graph[mention_id].add(parent_id)
	if mention_id not in outgoing_graph:
		outgoing_graph[mention_id]=set()
	
def cal_doc_page_rank(fileloc):
	global resultDict
	resultDict=defaultdict(float)
	loadTweets(fileloc)
        results=calculate_pagerank()
	for elem in results:
		resultDict[logical_no_to_user_id[elem[0]]]=elem[1]
	return resultDict

def main():
        print "start"
        #signal.signal(signal.SIGINT, handler)
        fileloc="../../mars_tweets_medium.json"
        loadTweets(fileloc)
        results=calculate_pagerank()
	printResult(results,50)
        print "done"


if __name__ == '__main__':
        main()


