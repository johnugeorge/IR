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

def loadTweets(fileloc):
        data=[]
	count=1
        json_data=open(fileloc,'r')
        buf=json_data.readlines()
        json_data.close()
        for line in buf:
                data=json.loads(line)
		tokens=re.findall(r"[\w]+", data['text'],re.UNICODE)
		#print data['text'].encode('utf8')
		id_val=data['id']
		doc_id_to_text[id_val]=data['text']
		doc_id_to_user_id[id_val]=data['user']['id']
		add_values_to_dict(tokens,id_val)
		#if count == 4:
		#	break
		#count+=1
	total_docs=len(main_dict)
	calculate_idf_value(total_docs)
	#print len(main_dict)
	#print len(document_freq_dict)
	#print main_dict
	calculate_tf_idf_value()
	#print main_dict
	normalize_tf_idf_value()

def normalize_tf_idf_value():
	global main_dict
	for doc in main_dict:
		square=0
		for term in main_dict[doc]:
			#print  main_dict[doc][term] , term
			square=square+ main_dict[doc][term]* main_dict[doc][term]
		#print "square",square," doc ",doc
		if square == 0:
			continue
		sq_root=math.sqrt(square)
		for term in main_dict[doc]:
			value= main_dict[doc][term]
			main_dict[doc][term]=value/sq_root



def calculate_tf_idf_value():
	for doc in main_dict:
		for term in main_dict[doc]:
			value= main_dict[doc][term]
			main_dict[doc][term]=value*document_freq_dict[term]
	

def printdict():
	print " Term Frequency Table "
	for doc in main_dict:
		print " Doc ", doc
		for term in main_dict[doc]:
			print "Key " , term.encode('utf8') ," Result ", main_dict[doc][term]
	print " Document Frequency table "
	for term in document_freq_dict:
		print "Key " , term.encode('utf8') ," Result ", document_freq_dict[term] 

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

def calculate_tf_value(id_val):
	for token in main_dict[id_val]:
		value=main_dict[id_val][token]
		main_dict[id_val][token]=1+math.log(value,2)
	#	print "Id val",id_val," token ", token, " value ",value," New Value ", main_dict[id_val][token]

def calculate_idf_value(total_docs):
	for token in document_freq_dict:
		value=document_freq_dict[token]
		document_freq_dict[token]=math.log(total_docs/value,2)
       
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
			print " Word not in Tweet Corpus "
			return 0
		square+=query_dict[token] * query_dict[token]
	if square==0:
		return 2
        sq_root=math.sqrt(square)
        for token in query_dict:
                token=token.lower()
                value= query_dict[token]
                query_dict[token]=value/sq_root
	print query_dict
	return 1

def calculate_cosine_values():
	global resultSet
	resultSet=defaultdict(float)
	for doc in main_dict:
		value=0
		for token in query_dict:
			if token in main_dict[doc]:
				#print " doc ",doc,"token ",token ,"Query term ",query_dict[token], " Main Dict value ",main_dict[doc][token]
				value=value+query_dict[token]*main_dict[doc][token]
		if value > 0:
			resultSet[doc]=value
	results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
	return results
				
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
	#print len(returnSet)
        return returnSet


def main():
        print "start"
        signal.signal(signal.SIGINT, handler)
        fileloc="../../mars_tweets_medium.json"
        loadTweets(fileloc)
	while 1:
		search_string=raw_input('Enter your search string here.(Press CTRL+C to quit) :')
		ret =parse_and_compute(search_string) 
		if ret == 0:
			print "Not Found "
			continue
		results=calculate_cosine_values()
		printResults(results,50)
        print "done"


if __name__ == '__main__':
        main()


