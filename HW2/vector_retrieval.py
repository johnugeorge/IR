import re
import signal
import sys
import json
import math
import bisect
from collections import defaultdict

def innerdict():
        return defaultdict(float)

main_dict=defaultdict(innerdict)
query_dict=defaultdict(float)
document_freq_dict=defaultdict(float)
doc_id_to_text=defaultdict(str)
resultSet=defaultdict(float)
doc_id_to_user_id=defaultdict(int)

def handler(signal, frame):
        print 'You pressed Ctrl+C!..Quiting'
        sys.exit(0)
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
		id_val=data['id']
		doc_id_to_text[id_val]=data['text']
		doc_id_to_user_id[id_val]=data['user']['id']
		add_values_to_dict(tokens,id_val)
	total_docs=len(main_dict)
	calculate_idf_value(total_docs)
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
Module to print whole dictionary
'''	

def printdict():
	print " Term Frequency Table "
	for doc in main_dict:
		print " Doc ", doc
		for term in main_dict[doc]:
			print "Key " , term.encode('utf8') ," Result ", main_dict[doc][term]
	print " Document Frequency table "
	for term in document_freq_dict:
		print "Key " , term.encode('utf8') ," Result ", document_freq_dict[term] 

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
Module to calculate idf value for each term
'''

def calculate_idf_value(total_docs):
	for token in document_freq_dict:
		value=document_freq_dict[token]
		document_freq_dict[token]=math.log(total_docs/value,2)
       
'''
Module to parse query and compute tf-idf value
'''
def parse_and_compute(query):
	global query_dict
        query_dict=defaultdict(float)
	square=0
	tokens=re.findall(r"[\w]+", query,re.UNICODE)
	for token in tokens:
                token=token.lower()
                query_dict[token]+=1
	for token in query_dict:
                token=token.lower()
                value=query_dict[token]
                value=1+math.log(value,2)
		if token in document_freq_dict:
                	query_dict[token]=value*document_freq_dict[token]
		else:
			print " Word/Words of Query not in Tweet Corpus "
			return 0
		square+=query_dict[token] * query_dict[token]
	if square==0:
		return 2
        sq_root=math.sqrt(square)
        for token in query_dict:
                token=token.lower()
                value= query_dict[token]
                query_dict[token]=value/sq_root
	return 1

'''
Module to find cosine similarity values between two vectors
'''
def calculate_cosine_values():
	global resultSet
	resultSet=defaultdict(float)
	for doc in main_dict:
		value=0
		for token in query_dict:
			if token in main_dict[doc]:
				value=value+query_dict[token]*main_dict[doc][token]
		if value > 0:
			resultSet[doc]=value
	results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
	return results

'''
Module to print Results 
'''				
def printResults(results,no_of_results):
	global doc_id_to_text
	count=1
        for doc in reversed(results):
		print "Rank ",count," Value ",doc[1]
                print "Tweet Id in Corpus: ",doc[0]
		print "Tweet Text: ",doc_id_to_text[doc[0]].encode('utf-8')
		print
                if count== no_of_results:
                        break
                count+=1
'''
Module exported to other modules to calculate cosine similarity values
between query and tweets
'''		
def cal_tf_idf_value(fileloc,search_string):
	returnSet=defaultdict(list)
	ret =parse_and_compute(search_string)
	if ret == 0:
		return returnSet
	results=calculate_cosine_values()
	for doc in reversed(results):
		tweet_id=doc[0]
		returnSet[tweet_id].append(doc[1])
		returnSet[tweet_id].append(doc_id_to_user_id[doc[0]])
		returnSet[tweet_id].append(doc_id_to_text[doc[0]])
        return returnSet


def main():
        print "Loading Tweets from Json Files"
	print
        signal.signal(signal.SIGINT, handler)
        fileloc="mars_tweets_medium.json"
        loadTweets(fileloc)
	while 1:
		search_string=raw_input('Enter your search string here.(Press CTRL+C to quit) :')
		ret =parse_and_compute(search_string) 
		if ret == 0:
			#print "  Not Found "
			print
			continue
		results=calculate_cosine_values()
		printResults(results,50)
        print "done"


if __name__ == '__main__':
        main()


