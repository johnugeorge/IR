#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import requests
from collections import defaultdict

pgIndex=0
uniqueWords=set()
pages=defaultdict(tuple)


def search():
  filenm = open('texasaggies.json', 'a')

  print 'texas aggies'
  r = requests.get('https://api.datamarket.azure.com/Bing/Search/News?Query=%27texas%20aggies%27&$format=json&$skip=0', auth=('johnu_george109', 'JyTOL4IYAo/KFJ65aWVAsWlqj/CKfGfXjX7sku386Mc='))
  i=1
  for obj in json.loads(r.text)['d']['results']:
    print i
    i+=1
    json.dump(obj,filenm)
    filenm.write('\n')

  print 'texas aggies'
  r = requests.get('https://api.datamarket.azure.com/Bing/Search/News?Query=%27texas%20aggies%27&$format=json&$skip=15', auth=('johnu_george109', 'JyTOL4IYAo/KFJ65aWVAsWlqj/CKfGfXjX7sku386Mc='))
  i=1
  for obj in json.loads(r.text)['d']['results']:
    print i
    i+=1
    json.dump(obj,filenm)
    filenm.write('\n')

  print 'texas longhorns'
  r = requests.get('https://api.datamarket.azure.com/Bing/Search/News?Query=%27texas%20longhorns%27&$format=json&$skip=0', auth=('johnu_george109', 'JyTOL4IYAo/KFJ65aWVAsWlqj/CKfGfXjX7sku386Mc='))
  i=1
  for obj in json.loads(r.text)['d']['results']:
    print i
    i+=1
    json.dump(obj,filenm)
    filenm.write('\n')

  print 'texas longhorns'
  r = requests.get('https://api.datamarket.azure.com/Bing/Search/News?Query=%27texas%20longhorns%27&$format=json&$skip=15', auth=('johnu_george109', 'JyTOL4IYAo/KFJ65aWVAsWlqj/CKfGfXjX7sku386Mc='))
  i=1
  for obj in json.loads(r.text)['d']['results']:
    print i
    i+=1
    json.dump(obj,filenm)
    filenm.write('\n')

  print 'duke blue devils'
  r = requests.get('https://api.datamarket.azure.com/Bing/Search/News?Query=%27duke%20blue%20devils%27&$format=json&$skip=0', auth=('johnu_george109', 'JyTOL4IYAo/KFJ65aWVAsWlqj/CKfGfXjX7sku386Mc='))
  i=1
  for obj in json.loads(r.text)['d']['results']:
    print i
    i+=1
    json.dump(obj,filenm)
    filenm.write('\n')

  print 'duke blue devils'
  r = requests.get('https://api.datamarket.azure.com/Bing/Search/News?Query=%27duke%20blue%20devils%27&$format=json&$skip=15&$top=15', auth=('johnu_george109', 'JyTOL4IYAo/KFJ65aWVAsWlqj/CKfGfXjX7sku386Mc='))
  i=1
  for obj in json.loads(r.text)['d']['results']:
    print i
    i+=1
    json.dump(obj,filenm)
    filenm.write('\n')

  print 'dallas cowboys'  
  r = requests.get('https://api.datamarket.azure.com/Bing/Search/News?Query=%27dallas%20cowboys%27&$format=json&$skip=0', auth=('johnu_george109', 'JyTOL4IYAo/KFJ65aWVAsWlqj/CKfGfXjX7sku386Mc='))
  i = 1
  for obj in json.loads(r.text)['d']['results']:
    print i
    i+=1
    json.dump(obj,filenm)
    filenm.write('\n')

  print 'dallas cowboys'
  r = requests.get('https://api.datamarket.azure.com/Bing/Search/News?Query=%27dallas%20cowboys%27&$format=json&$skip=15', auth=('johnu_george109', 'JyTOL4IYAo/KFJ65aWVAsWlqj/CKfGfXjX7sku386Mc='))
  i = 1
  for obj in json.loads(r.text)['d']['results']:
    print i
    i+=1
    json.dump(obj,filenm)
    filenm.write('\n')

  print 'dallas mavericks'
  r = requests.get('https://api.datamarket.azure.com/Bing/Search/News?Query=%27dallas%20mavericks%27&$format=json&$skip=0', auth=('johnu_george109', 'JyTOL4IYAo/KFJ65aWVAsWlqj/CKfGfXjX7sku386Mc='))
  i = 1
  for obj in json.loads(r.text)['d']['results']:
    print i
    i+=1
    json.dump(obj,filenm)
    filenm.write('\n')

  print 'dallas mavericks'
  r = requests.get('https://api.datamarket.azure.com/Bing/Search/News?Query=%27dallas%20mavericks%27&$format=json&$skip=15', auth=('johnu_george109', 'JyTOL4IYAo/KFJ65aWVAsWlqj/CKfGfXjX7sku386Mc='))
  i = 1
  for obj in json.loads(r.text)['d']['results']:
    print i
    i+=1
    json.dump(obj,filenm)
    filenm.write('\n')


#    filenm.write('\n')
#    jsonobj = r.json()
#    json.dump(jsonobj,filenm)
#    filenm.write('\n')
#    parseJson(jsonobj)
  filenm.close()
  return

def parseJson(jsonobj):    
    for page in jsonobj['d']['results']:
        completeStr = page['Title'] + ' ' + page['Description']
	tokens=re.findall('\w+', completeStr.lower(),re.UNICODE)
        for word in tokens:
           uniqueWords.add(word)

def main():
  search()

if __name__ == '__main__':
  main()


