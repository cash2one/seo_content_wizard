### SEO Content Wizard by Slava Rybalka on May, 2016
### Python 3.4.2

### 1. Get Top 10 search results on Google for a keyword. - done
### 2. Analyze the contents of these pages. - done
### 3. Build a dictionary of keyword phrases, sorted by frequency of occurence.
### 4. Check if any of the top keywords is in the page we are trying to rank for this keyword.
### 5. Assign a score to our page.
# -*- coding: utf-8 -*-


import urllib
import http.client
from urllib.parse import urlparse
import urllib.request
from urllib.error import URLError, HTTPError
import socket
from socket import timeout
import re
import time
import sys
import codecs
import string
import collections
import itertools

if sys.stdout.encoding != 'utf-8':
  sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'utf-8':
  sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

keyword = "property management software"
simple_query = "https://www.google.com/search?num=100&ion=1&espv=&ie=UTF-8&q="
opener = urllib.request.FancyURLopener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
socket.setdefaulttimeout(10)
new_links = []
super_graph_two = [] # combined list of 2-word phrases
super_graph_three = [] # combined list of 3-word phrases

#####################
# Request to Google #
#####################


try:
   se_req = opener.open(simple_query + keyword.replace(' ','%20'))
   results = se_req.read()
   with open('test.txt', mode='w', encoding='utf-8') as a_file:
     a_file.write(results.decode("UTF-8"))               
   #print(results)
   links = re.findall(b'bottom:2px"><cite>([^"]+)</cite>', results)
   for i in links[:10]: # set how many top results you need here
     i = re.sub("<.*?>", "", i.decode("UTF-8")) # removing HTML tags, and turing the object into a string
     new_links.append(i)
     
except HTTPError as e:
   print('HTTP error:', e.code)
   pass
except URLError as e:
   print('We failed to reach a server:', e.reason)
   pass
except socket.timeout:
   print('socket timeout')
   pass
except http.client.BadStatusLine as e:
   print('HTTP error not recognized, error code not given')
   pass
except ValueError as e:
   print('Error:', e)
   pass

def query_url(url):
  url = "http://" + url.replace("http://",'').replace("https://",'') # sanitizing the URI
  #print(url)
  request = opener.open(url)
  results = request.read()
  return results


def find_2_words_phrases(pagecontents):
  x = pagecontents.decode('UTF-8').replace('\r','').replace('\n','').replace('\t','').split(' ')
  new_list = list(filter(None, x)) # removing empty elements from the list
  two_words_list = list(zip(new_list, new_list[1:]))
  return two_words_list


def find_3_words_phrases(pagecontents):
  x = pagecontents.decode('UTF-8').replace('\r','').replace('\n','').replace('\t','').split(' ')
  new_list = list(filter(None, x)) # removing empty elements from the list
  three_words_list = list(zip(new_list, new_list[1:], new_list[2:]))
  return three_words_list


#############
# Execution #
#############


for elem in new_links: # iterating through the list of Top 10 web pages ranking for the keyword
  z = re.sub("<.*?>", "", elem) # removing html tags from the list of website URLs
  content_of_the_page = query_url(z) # get contents of every URL from the list

  super_graph_two.append(find_2_words_phrases(content_of_the_page)) # adds all 2-word combinations on the page to the super list
  super_graph_three.append(find_3_words_phrases(content_of_the_page)) # adds all 3-word combinations on the page to the super list
  
  print(elem) # prits the URL being processed

print(len(super_graph_two))
print(len(super_graph_three[0]), len(super_graph_three[1]), len(super_graph_three[2]))

graph_2_word = [item for sublist in super_graph_two for item in sublist]
graph_3_word = [item for sublist in super_graph_three for item in sublist]
print(graph_3_word[34])
y = collections.Counter(graph_2_word)
xvv = itertools.islice(y.items(), 0, 4)
print(xvv)