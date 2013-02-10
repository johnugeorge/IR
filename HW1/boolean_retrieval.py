import os
import re
from collections import defaultdict

new_hash=defaultdict(set)

def build_index():
	dir='books'
	filenames = os.listdir(dir)
	for filename in filenames:
	        rel_path=os.path.join(dir, filename)
		match=re.search(r'([\d]+).txt', filename)
                if match:
			doc_Id= match.group(1)
		f = open(rel_path, 'rU')
		#print filename,doc_Id
		buf=f.read()
                tokens=re.findall(r"[\w]+", buf)
		add_Inverted_Index(doc_Id,tokens)
		f.close()
	print " Total Inverted Index Keys ",len(new_hash)
	
def add_Inverted_Index(doc_Id,tokens):
	for token in tokens:
		token=token.lower()
		new_hash[token].add(doc_Id)

def get_Inverted_Index():
	build_index()
	return new_hash

def searchfn():
	while(1):
		search_string=raw_input('Enter your search string here: ')
	        search_list=search_string.split()
	        print search_string,search_list
	        new_list=[]
	        result_found=0
	        for elem in search_list:
			if elem in new_hash:
				result_found=1;
			        new_list.append(new_hash[elem])
		        else:
			        result_found=0
			        break
                if result_found:
		        result =set(new_list[0]).intersection(*new_list[1:])
		        print result
	        else:
		        print "sorry no match :("

def search(query):
	if query in new_hash:
		return new_hash[query]
	else:
		return []

def main():
	print "Loading Index"
	build_index()
	searchfn()


if __name__ == '__main__':
	main()
