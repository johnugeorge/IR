import re
import signal
import sys
import json
import math
from collections import defaultdict

def innerdict():
        return defaultdict(float)

main_dict=defaultdict(innerdict)
query_dict=defaultdict(float)
document_freq_dict=defaultdict(float)

def handler(signal, frame):
        print main_dict[doc][term]
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
		#print data
		tokens=re.findall(r"[\w]+", data['text'],re.UNICODE)
#		tokens=re.split(" |'|\"", data['text'],re.UNICODE)

		id_val=data['id']
		#print id_val
		add_values_to_dict(tokens,id_val)
		if count == 4:
			break
		count+=1
	printdict()
	total_docs=len(main_dict)
	calculate_idf_value(total_docs)
	print len(main_dict)
	print len(document_freq_dict)
	#printdict()
	calculate_tf_idf_value()
	normalize_tf_idf_value()
	#printdict()
	#print document_freq_dict
                #data.append(json.loads(line))
def normalize_tf_idf_value():
	for doc in main_dict:
		square=0;
		for term in main_dict[doc]:
			square=square+ main_dict[doc][term]* main_dict[doc][term]
		sq_root=math.sqrt(square)
		print sq_root, square	
		for term in main_dict[doc]:
			value= main_dict[doc][term]
			main_dict[doc][term]=value/sq_root



def calculate_tf_idf_value():
	for doc in main_dict:
		for term in main_dict:
			value= main_dict[doc][term]
			main_dict[doc][term]=value*document_freq_dict[term]
	

def printdict():
	for doc in main_dict:
		print " Doc ", doc
		print 
		for term in main_dict[doc]:
			print "Key " , term ," Result ", main_dict[doc][term]
			print 

def add_values_to_dict(tokens,id_val):
	for token in tokens:
		token=token.lower()
		
		main_dict[id_val][token]+=1
	list_of_tokens=list(set(tokens))
	for elem in list_of_tokens:
		document_freq_dict[elem]+=1
	calculate_tf_value(id_val)
	return
	#maindict[

def calculate_tf_value(id_val):
	for token in main_dict[id_val]:
		value=main_dict[id_val][token]
		main_dict[id_val][token]=1+math.log(value,2)
		print "Id val",id_val," token ", token, " value ",value," New Value ", main_dict[id_val][token]

def calculate_idf_value(total_docs):
	for token in document_freq_dict:
		value=document_freq_dict[token]
		document_freq_dict[token]=math.log(total_docs/value,2)
       
def parse_and_compute(query):
	square=0
	tokens=re.findall(r"[\w]+", query,re.UNICODE)
	for token in tokens:
                token=token.lower()
                query_dict[token]+=1
	for token in query_dict:
                value=query_dict[token]
                value=1+math.log(value,2)
                query_dict[token]=value*document_freq_dict[token]
		square+=query_dict[token] * query_dict[token]
        sq_root=math.sqrt(square)
	print sq_root, square
        for token in query_dict:
                value= query_dict[token]
                query_dict[token]=value/sq_root


def main():
        print "start"
        #signal.signal(signal.SIGINT, handler)
        fileloc="../../mars_tweets_medium.json"
        loadTweets(fileloc)
	search_string=raw_input('Enter your search string here.(Press CTRL+C to quit) :')
	parse_and_compute(search_string)
        print "done"


if __name__ == '__main__':
        main()


