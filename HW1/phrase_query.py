import os
import re
import copy
from collections import defaultdict

token_to_docId=defaultdict(list)
result_docId=[]
def build_index():
	dir='books'
	filenames = os.listdir(dir)
	#filenames =['70.txt','119.txt']
	for filename in filenames:
		print "Filename",filename
	        rel_path=os.path.join(dir, filename)
		match=re.search(r'([\d]+).txt', filename)
                if match:
			doc_Id= match.group(1)
		f = open(rel_path, 'rU')
		#print filename,doc_Id
		buf=f.read()
		#buf= " this is a fun this is"
		add_Positional_Index(doc_Id,buf)
		f.close()
		#break
	print " Total Keys ",len(token_to_docId)
	
def add_Positional_Index(doc_Id,buf):
        tokens=re.findall(r"[\w]+", buf)
	count=0
	for token in tokens:
        #for match in re.finditer(r"[\w]+", buf):
		#word=match.group()
		word=token
                docId_to_pos=defaultdict(list)
		word=word.lower()
		if not word in token_to_docId:
			#docId_to_pos[doc_Id].append(match.start())
			docId_to_pos[doc_Id].append(count)
		        token_to_docId[word]=docId_to_pos
		else:
			#token_to_docId[word][doc_Id].append(match.start())
			token_to_docId[word][doc_Id].append(count)
	        count +=1
	
        #print token_to_docId.items()


def phrase_query(phrase):
	list_of_docIds_per_phrase=[]
	result_found=1
	tokens=re.findall(r"[\w]+", phrase)
	final_result=[]
	print "TOKENS",tokens
	positonal_lists=[]
	temp_list=[]
	for token in tokens:
		token=token.lower()
		if token in token_to_docId:
			#print token,"If"
			list_of_docIds_per_phrase.append([x for x in token_to_docId[token]])
			#print list_of_docIds_per_phrase
		else:
			#print token,"else"
			result_found=0
			return 0
	if result_found != 0:
		common_docId_list =set(list_of_docIds_per_phrase[0]).intersection(*list_of_docIds_per_phrase[1:])
	        #print common_docId_list, tokens,token_to_docId
	else:
		print "no match"
	count=0
	for token in tokens:
		token=token.lower()
		for doc in common_docId_list:
			#print " doc ",doc 
			token_to_docId[token][doc]=([x-count for x in token_to_docId[token][doc]])
		count +=1
	for doc in common_docId_list:
		temp_list=[]
		for token in tokens:
			temp_list.append(token_to_docId[token][doc])
			print "doc",doc,"token",token,"temp list",temp_list
                final_positional_list=set(temp_list[0]).intersection(*temp_list[1:])
		print final_positional_list
		if final_positional_list:
			result_docId.append(doc)
	print "-----------Result-----------", result_docId



def searchfn():
	while(1):
		search_string=raw_input('Enter your search string here: ')
	        search_list=search_string.split("\"")
		final_list=[]
		for elem in search_list:
			if elem:
				final_list.append(elem.strip())
	        print final_list
	        result_found=0
		for elem in final_list:
			ret = phrase_query(elem)
			if ret == 0: break
                #if result_found:
		#        result =set(new_list[0]).intersection(*new_list[1:])
		#        print result
	        #else:
		#        print "sorry no match :("


def main():
	print "Loading Index"
	build_index()
	searchfn()


if __name__ == '__main__':
	main()
