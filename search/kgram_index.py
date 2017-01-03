import os
import re
import copy
from collections import defaultdict
import boolean_retrieval
import pickle

kgram_index= defaultdict(set)
inverted_index=defaultdict(set)


def build_index():
        dir='books'
        filenames = os.listdir(dir)
        for filename in filenames:
                rel_path=os.path.join(dir, filename)
                match=re.search(r'([\d]+).txt', filename)
                if match:
                        doc_Id= match.group(1)
                f = open(rel_path, 'rU')
                buf=f.read()
                add_kgram_Index(doc_Id,buf)
                f.close()
        #print " Total Keys ",len(kgram_index)

def add_kgram_Index(doc_Id,buf):
        tokens=re.findall(r"[\w]+", buf)
        for token in tokens:
		token=token.lower()
		token="".join(re.findall("[a-zA-Z0-9]+", token))
        	count=0
		temp_string="$"+token+"$"
		while count < len(temp_string)-1:
			bi_gram= temp_string[count:count+2]
			kgram_index[bi_gram].add(token)
			count +=1

def add_k_gram_Index_prebuilt(dir='books'):
	global inverted_index
	global kgram_index
	inverted_index=boolean_retrieval.get_Inverted_Index(dir)
#	if os.path.exists("kgram_index.pickle"):
#		print "Loading from kgram_index.pickle "
#		kgram_index = pickle.load( open( "kgram_index.pickle", "rb" ) )
 #       	print " Total K_Gram Keys ",len(kgram_index)
#		return
	for token in inverted_index.keys():
		count=0
                temp_string="$"+token+"$"
                while count < len(temp_string)-1:
			bi_gram= temp_string[count:count+2]
                        kgram_index[bi_gram].add(token)
                        count +=1
	if not os.path.exists("kgram_index.pickle"):
		print "creating kgram_index.pickle "
		pickle.dump( kgram_index, open( "kgram_index.pickle", "wb" ) )
        #print " Total K_Gram Keys ",len(kgram_index)

			
def kgram_query(elem):
	 temp_string=[]
	 match_string=[]
	 result_words=set([])
	 result_docId_list=[]
	 present=0
	 end=0
	 start=0
	 list_of_bigrams=[]
	 if elem.startswith("*"):
	 	 present=1
	 	 word="".join(re.findall("[a-zA-Z0-9]+", elem))
		 temp_string.append(word + "$")
		 match_string.append(word)
		 start=1
	 elif elem.endswith("*"):
	 	 present=1
	 	 word="".join(re.findall("[a-zA-Z0-9]+", elem))
		 temp_string.append("$" + word)
		 match_string.append(word)
		 end=1
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
	 for word in common_word_list:
		 if start==1:
			 val=match_string[0]
			 if word.endswith(val):
				 result_words.add(word)
	         elif end==1:
			 val=match_string[0]
		         if word.startswith(val):
				 result_words.add(word)
		 else:
			 if len(match_string)==2:
				 val1=match_string[0]
				 val2=match_string[1]
				 if word.startswith(val1) and word.endswith(val2) and len(word)>=2:
					 result_words.add(word)
			 else:
				 print " Error * not found in middle "

	 for word in result_words:
		 result_docId_list.append(inverted_index[word])
	 final_docId_list =set(result_docId_list[0]).union(*result_docId_list[1:])
	 return final_docId_list


def search(query):
	result=kgram_query(query)
	new_list=[ x for x in iter(result) ]
	return new_list

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
                        ret = kgram_query(elem)
                        if ret == 0: break


def main():
        print "Loading Index"
	add_k_gram_Index_prebuilt()
        searchfn()


if __name__ == '__main__':
        main()
