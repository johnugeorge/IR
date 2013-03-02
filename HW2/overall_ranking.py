import re
import signal
import sys
import json
import math
import bisect
import vector_retrieval
import page_rank
from collections import defaultdict

user_wt=0.3
def handler(signal, frame):
        print 'You pressed Ctrl+C!..Quiting'
        sys.exit(0)


def printResults(results,cosine_results,no_of_results):
        count=1
        for doc in reversed(results):
                print "Rank ",count," Final Score ",doc[1]
                print "Tweet Id in Corpus: ",doc[0]
		#if (cosine_results[doc[0]]): 
                #	print "Tweet Text: ",(cosine_results[doc[0]])[2]
                print "Tweet Text: ",(cosine_results[doc[0]])[2].encode('utf-8')
                print
                if count== no_of_results:
                        return
                count+=1


def main():
        print "start"
	page_rank_results=defaultdict(float)
	cosine_results =defaultdict(list)
        signal.signal(signal.SIGINT, handler)
        fileloc="../../mars_tweets_medium.json"
	#fileloc="test2.query"
	sum_total=0.0
	page_rank_results=page_rank.cal_doc_page_rank(fileloc)
	for elem in page_rank_results:
		#print page_rank_results
		sum_total=sum_total+page_rank_results[elem]
	print " Total Sum ",sum_total,len(page_rank_results)
	vector_retrieval.loadTweets(fileloc)
	while 1:
		updated_score_result=defaultdict(float)
		search_string=raw_input('Enter your search string here.(Press CTRL+C to quit) :')
		cosine_results = vector_retrieval.cal_tf_idf_value(fileloc,search_string)
		print len(cosine_results)
		if len(cosine_results) < 10:
			print cosine_results
		for doc in cosine_results:
			#print "doc:" ,doc,"Results", cosine_results[doc]
			user_id=(cosine_results[doc])[1]
			user_page_rank=page_rank_results[user_id]
			#print user_id , user_page_rank
			normalized_pr=user_page_rank/sum_total
			score= (user_wt)*normalized_pr + (1 - user_wt)*(cosine_results[doc])[0]
			updated_score_result[doc]=score
		results=[(key,val) for key, val in sorted(updated_score_result.iteritems(), key=lambda (k,v): (v,k))]
		printResults(results,cosine_results,10)			
        print "done"


if __name__ == '__main__':
        main()


