import os
import re
import copy
from collections import defaultdict
import boolean_retrieval

kgram_index= defaultdict(set)
inverted_index=defaultdict(set)


def build_index():
        dir='books'
        filenames = os.listdir(dir)
        #filenames =['70.txt','119.txt']
        for filename in filenames:
                #print "Filename",filename
                rel_path=os.path.join(dir, filename)
                match=re.search(r'([\d]+).txt', filename)
                if match:
                        doc_Id= match.group(1)
                f = open(rel_path, 'rU')
                #print filename,doc_Id
                buf=f.read()
                #buf= " this is a fun this is.I dont know what when woow to do.worn Lets see one examaple and decide"
                add_kgram_Index(doc_Id,buf)
                f.close()
                #break
        print " Total Keys ",len(kgram_index)

def add_kgram_Index(doc_Id,buf):
        tokens=re.findall(r"[\w]+", buf)
        for token in tokens:
		token=token.lower()
        	count=0
		temp_string="$"+token+"$"
		while count < len(temp_string)-1:
			bi_gram= temp_string[count:count+2]
			kgram_index[bi_gram].add(token)
			count +=1
	#print kgram_index

def add_k_gram_Index_prebuilt():
	global inverted_index
	inverted_index=boolean_retrieval.get_Inverted_Index()
	for token in inverted_index.keys():
		count=0
                temp_string="$"+token+"$"
                while count < len(temp_string)-1:
			bi_gram= temp_string[count:count+2]
                        kgram_index[bi_gram].add(token)
                        count +=1
        print " Total K_Gram Keys ",len(kgram_index)





			
def kgram_query(elem):
	 temp_string=[]
	 match_string=[]
	 result_words=set([])
	 result_docId_list=[]
	 present=0
	 list_of_bigrams=[]
	 if elem.startswith("*"):
	 	 present=1
	 	 word="".join(re.findall("[a-zA-Z0-9]+", elem))
		 temp_string.append(word + "$")
		 match_string.append(word)
	 elif elem.endswith("*"):
	 	 present=1
	 	 word="".join(re.findall("[a-zA-Z0-9]+", elem))
		 temp_string.append("$" + word)
		 match_string.append(word)
	 else:
	         match = re.search(r'([a-zA-Z0-9]+)\*([a-zA-Z0-9]+)', elem)
		 if match:
	 	 	 present=1
			 #print match.group(1),match.group(2)
			 temp_string.append("$" + match.group(1))
			 temp_string.append(match.group(2)+ "$")
			 match_string.append(match.group(1))
			 match_string.append(match.group(2))
         if present==0:
		 print "Not a wildcard query "
		 temp_string.append(elem)
		 list_of_bigrams.append([])
	 for val in temp_string:
		 count = 0
		 while count < len(val)-1:
			 bi_gram= val[count:count+2]
			 list_of_bigrams.append(kgram_index[bi_gram])
			 count +=1
	 common_word_list =set(list_of_bigrams[0]).intersection(*list_of_bigrams[1:])
	 #print common_word_list
	 for word in common_word_list:
		 for val in match_string:
			if(word.find(val) != -1):
				 result_words.add(word)
	 #print result_words
	 for word in result_words:
		 #print word
		 result_docId_list.append(inverted_index[word])
	 #print result_docId_list
	 final_docId_list =set(result_docId_list[0]).union(*result_docId_list[1:])
         #print final_docId_list
	 return final_docId_list


def search(query):
	result=kgram_query(query)
	new_list=[ x for x in iter(result) ]
	return new_list

def searchfn():
        while(1):
                search_string=raw_input('Enter your search string here: ')
#		temp_string=
#		for x in search_string:
#			if x=="\"":
				
                search_list=search_string.split("\"")
                final_list=[]
                for elem in search_list:
                        if elem:
                                final_list.append(elem.strip())
                #print final_list
                result_found=0
                for elem in final_list:
                        ret = kgram_query(elem)
                        if ret == 0: break
                #if result_found:
                #        result =set(new_list[0]).intersection(*new_list[1:])
                #        print result
                #else:
                #        print "sorry no match :("


def main():
        print "Loading Index"
	add_k_gram_Index_prebuilt()
        #build_index()
        searchfn()


if __name__ == '__main__':
        main()
