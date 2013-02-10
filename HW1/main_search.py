import re
import boolean_retrieval
import phrase_query
import kgram_index
import signal
import sys

def handler(signal, frame):
	print
	print 'You pressed Ctrl+C!..Quiting'
	sys.exit(0)

def searchfn():
	print "Loading Indexes"
	print
	kgram_index.add_k_gram_Index_prebuilt()
	phrase_query.build_index()
	print " Indexes Loaded "
	print
        while(1):
		search_string=raw_input('Enter your search string here.(Press CTRL+C to quit) :')
		temp_string=""
		str_without_positional_queries=""
		formatted_list=[]
		positional_queries=[]
		kgram_queries=[]
		boolean_queries=[]
		result_list=[]
		kgram=0
                for char in search_string:
			if char != "\"" and kgram == 1:
				temp_string=temp_string+char
			elif char == "\"" and kgram == 0:
				kgram=1;
			elif char == "\"" and kgram ==1:
				str_without_positional_queries=str_without_positional_queries+" ";
				positional_queries.append(temp_string)
				temp_string=""
				kgram=0
			else:
				str_without_positional_queries=str_without_positional_queries+char;
		#print str_without_positional_queries
		formatted_word=" ".join(re.findall("[a-zA-Z0-9*]+", str_without_positional_queries))
                #print formatted_word
		formatted_list=formatted_word.split(" ")
		#print formatted_list
		for word in formatted_list:
			if word:
				if word.find("*") == -1 :
					boolean_queries.append(word)
				else:
					kgram_queries.append(word)

		print "Phrase Queries: ",positional_queries
		print "WildCard Queries:",kgram_queries
		print "Boolean Queries: ",boolean_queries
		for elem in boolean_queries:
			result=boolean_retrieval.search(elem)
			result_list.append(result)
		for elem in positional_queries:
			result=phrase_query.search(elem)
			result_list.append(result)
		for elem in kgram_queries:
			result=kgram_index.search(elem)
			result_list.append(result)
	       	if len(result_list) > 0:
			common_word_list =set(result_list[0]).intersection(*result_list[1:])
		else:
			common_word_list=set([])
		printresult(common_word_list)

def printresult(result):
	if result:
		print 
		print "----- Result------"
		for elem in result:
			print elem," ",
	else:
		print "sorry no match :("
	print 
	print 

def main():
	signal.signal(signal.SIGINT, handler)
        searchfn()


if __name__ == '__main__':
        main()

