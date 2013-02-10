import os
import re
import copy
import pickle
from collections import defaultdict

token_to_docId= defaultdict(list)
result_dict   = defaultdict(list)
def build_index():
	global token_to_docId
#	if os.path.exists("phrase_query.pickle"):
#		print "Loading from phrase_query.pickle "
#                token_to_docId = pickle.load( open( "phrase_query.pickle", "rb" ) )
#		print " Total Postional Index Keys ",len(token_to_docId)
#                return
	dir='books'
	filenames = os.listdir(dir)
	for filename in filenames:
	        rel_path=os.path.join(dir, filename)
		match=re.search(r'([\d]+).txt', filename)
                if match:
			doc_Id= match.group(1)
		f = open(rel_path, 'rU')
		buf=f.read()
		add_Positional_Index(doc_Id,buf)
		f.close()
	if not os.path.exists("phrase_query.pickle"):
		print "creating phrase_query.pickle "
		pickle.dump( token_to_docId, open( "phrase_query.pickle", "wb" ) )
#	print " Total Postional Index Keys ",len(token_to_docId)
	
def add_Positional_Index(doc_Id,buf):
        tokens=re.findall(r"[\w]+", buf)
	count=0
	for token in tokens:
		word=token
                docId_to_pos=defaultdict(list)
		word=word.lower()
		word="".join(re.findall("[a-zA-Z0-9]+", word))
		if not word in token_to_docId:
			docId_to_pos[doc_Id].append(count)
		        token_to_docId[word]=docId_to_pos
		else:
			token_to_docId[word][doc_Id].append(count)
	        count +=1


def phrase_query(phrase):
	list_of_docIds_per_phrase=[]
	result_docId=[]
	result_found=1
	tokens=re.findall(r"[\w]+", phrase)
	final_result=[]
	positonal_lists=[]
	temp_list=[]
	for token in tokens:
		token=token.lower()
		if token in token_to_docId:
			list_of_docIds_per_phrase.append([x for x in token_to_docId[token]])
		else:
			result_found=0
			return 0
	if result_found != 0:
		common_docId_list =set(list_of_docIds_per_phrase[0]).intersection(*list_of_docIds_per_phrase[1:])

	else:
		print "no match"
	count=0
	for token in tokens:
		token=token.lower()
		for doc in common_docId_list:
                	docId_to_pos=defaultdict(list)
			if not token in result_dict:
				docId_to_pos[doc] = [x-count for x in token_to_docId[token][doc]]
		        	result_dict[token]=docId_to_pos
			else:
				result_dict[token][doc] = [x-count for x in token_to_docId[token][doc]]
		count +=1
	for doc in common_docId_list:
		temp_list=[]
		for token in tokens:
			temp_list.append(result_dict[token][doc])
                final_positional_list=set(temp_list[0]).intersection(*temp_list[1:])
		if final_positional_list:
			result_docId.append(doc)
	return result_docId

def search(query):
	result=phrase_query(query)
	return result



def searchfn():
	while(1):
		search_string=raw_input('Enter your search string here: ')
	        search_list=search_string.split("\"")
		final_list=[]
		for elem in search_list:
			if elem:
				final_list.append(elem.strip())
	        result_found=0
		for elem in final_list:
			ret = phrase_query(elem)
			if ret == 0: break


def main():
	print "Loading Index"
	build_index()
	searchfn()


if __name__ == '__main__':
	main()
