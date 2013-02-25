import re
import signal
import sys
import json
from collections import defaultdict

def innerdict():
        return defaultdict(float)

maindict=defaultdict(innerdict)

def handler(signal, frame):
        print
        print 'You pressed Ctrl+C!..Quiting'
        sys.exit(0)

def loadTweets():
        data=[]
        json_data=open('mars_tweets_medium.json','r')
        buf=json_data.readlines()
        json_data.close()
        for line in buf:
                data=json.loads(line)
                #data.append(json.loads(line))

        
def main():
        print "start"
        #signal.signal(signal.SIGINT, handler)
        loadTweets()
        print "done"


if __name__ == '__main__':
        main()


