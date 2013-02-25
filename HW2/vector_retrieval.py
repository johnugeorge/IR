import re
import signal
import sys
import json
from collections import defaultdict

def innerdict():
        return defaultdict(float)

main_dict=defaultdict(innerdict)
document_freq_dict=defaultdict(set)

def handler(signal, frame):
        print
        print 'You pressed Ctrl+C!..Quiting'
        sys.exit(0)

def loadTweets(fileloc):
        data=[]
        json_data=open(fileloc,'r')
        buf=json_data.readlines()
        json_data.close()
        for line in buf:
                data=json.loads(line)
		#print data
		tokens=re.findall(r"[\w]+", data['text'],re.UNICODE)
		id_val=data['id']
		#print id_val
		add_values_to_dict(tokens,id_val)
	print len(main_dict)
	print len(document_freq_dict)
                #data.append(json.loads(line))

def add_values_to_dict(tokens,id_val):
	for token in tokens:
		main_dict[id_val][token]+=1
		document_freq_dict[token].add(id_val)
	return
	#maindict[
	
        
def main():
        print "start"
        #signal.signal(signal.SIGINT, handler)
        fileloc="../../mars_tweets_medium.json"
        loadTweets(fileloc)
        print "done"


if __name__ == '__main__':
        main()


