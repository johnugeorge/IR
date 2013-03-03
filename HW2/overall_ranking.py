import re
import signal
import sys
import json
import math
import bisect
import vector_retrieval
import page_rank
from collections import defaultdict

user_wt=0.5
def handler(signal, frame):
        print 'You pressed Ctrl+C!..Quiting'
        sys.exit(0)

'''
Module to print results of integrated system
'''
def printResults(results,cosine_results,no_of_results):
        count=1
        for doc in reversed(results):
                print "Rank ",count," Final Score ",doc[1]
                print "Tweet Id in Corpus: ",doc[0]
                print "Tweet Text: ",(cosine_results[doc[0]])[2].encode('utf-8')
                print
                if count== no_of_results:
                        return
                count+=1


def main():
        print "Loading Tweets from Json File"
	print
	page_rank_results=defaultdict(float)
	cosine_results =defaultdict(list)
        signal.signal(signal.SIGINT, handler)
        fileloc="mars_tweets_medium.json"
	sum_total=0.0
	page_rank_results=page_rank.cal_doc_page_rank(fileloc)
	#for elem in page_rank_results:
	#	sum_total=sum_total+page_rank_results[elem]
	vector_retrieval.loadTweets(fileloc)
	while 1:
		updated_score_result=defaultdict(float)
		search_string=raw_input('Enter your search string here.(Press CTRL+C to quit) :')
		cosine_results = vector_retrieval.cal_tf_idf_value(fileloc,search_string)
		for result in cosine_results:
			user_id=(cosine_results[result])[1]
			user_page_rank=page_rank_results[user_id]
			sum_total=sum_total+user_page_rank
		for doc in cosine_results:
			user_id=(cosine_results[doc])[1]
			user_page_rank=page_rank_results[user_id]
			normalized_pr=user_page_rank/sum_total
			score= (user_wt)*normalized_pr + (1 - user_wt)*(cosine_results[doc])[0]
			updated_score_result[doc]=score
		results=[(key,val) for key, val in sorted(updated_score_result.iteritems(), key=lambda (k,v): (v,k))]
		printResults(results,cosine_results,10)		
		print	
        print "done"


if __name__ == '__main__':
        main()


