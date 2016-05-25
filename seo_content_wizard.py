### SEO Content Wizard by Slava Rybalka on May, 2016
### Python 3.4.2

### 1. Get Top 10 search results on Google for a keyword.
### 2. Analyze the contents of these pages.
### 3. Build a dictionary of keyword phrases, sorted by frequency of occurence.
### 4. Check if any of the top keywords is in the page we are trying to rank for this keyword.
### 5. Assign a score to our page.


import urllib
import http.client
from urllib.parse import urlparse
import urllib.request
from urllib.error import URLError, HTTPError
import socket
from socket import timeout
import re
import time

#clients_domain = input("Enter the domain starting with www or without it: ...")
keyword = input("Enter the keyword: ...")
simple_query = "https://www.google.com/search?num=100&ion=1&espv=&ie=UTF-8&q="
opener = urllib.request.FancyURLopener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
socket.setdefaulttimeout(10)

#print('Checking if any page of '+ clients_domain + ' is ranking on Google...\n')

##########--------Request to Google ----------###################

try:
   se_req = opener.open(simple_query + keyword.replace(' ','%20'))
   results = se_req.read()
   with open('test.txt', mode='w', encoding='utf-8') as a_file:
     a_file.write(results.decode("UTF-8"))               
   #print(results)
   links = re.findall(b'bottom:2px"><cite>([^"]+)</cite>', results)
   for i in links[:10]:
     i = re.sub("<.*?>", "", i.decode("UTF-8")) # removing HTML tags, and turing the object into a string
     print(i)


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