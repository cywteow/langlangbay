# -*- coding: utf-8 -*-
import json
import re
import sys
import urllib
import base64

import urllib2
import urlparse

def Get(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    return urllib2.urlopen(req).read()

langlangbayUrl = "https://langlangbay.org"

path = "test"

# page = Get(langlangbayUrl + "/cn/")
# it = re.finditer("<a href=\"(.*?)\">\n\t\t\t\t\t\t<div class=\"title sizing\">(.*?)</div>", page, flags=0)
# it2 = re.finditer("<div class=\"txttitle\">\n\t\t\t\t<a href=\"(.*?)\">(.*?)\(.*?\)</a>", page, flags=0)
# for matchObj in it2:
#     path = matchObj.group(1)
#     break

page2 = Get(langlangbayUrl + "/cn200910/")
it3 = re.finditer("<li class=\"sizing\"><h2><a rel=\"nofollow noopener noreferrer\" onclick=\"xxx\('(.*?)','(.*?)',(.*)>(.*?)</a>", page2, flags=0)
count = 0
for matchObj2 in it3:
    print(matchObj2.group(4)+", "+matchObj2.group(2))
    count += 1
if(count == 0):
    it3 = re.finditer("<li class=\"sizing\"><h2><a href=\"(.*?).html\">(.*?)</a></h2></li>",page2,flags=0)
    for matchObj2 in it3:
        print(matchObj2.group(2) + " - " + matchObj2.group(1))

# encryptedString = "==QfdJCNVNTT0VzQlxmUtJGc5MkT0kFVNpXSt5ka5wWT4tGVPZ3ZU1UNBRUT5FkaNZHMyIma1MVWrx2VkZDZtJmdoJjW1lzRaVHNXlVaWNjYrlTeMZTTINGMShUYRRWcE9lIbpjIzRWaiwiIuVXWaJiOiU2YyV3bzJye"
# encryptedString = "test"
# page = Get(langlangbayUrl + "/cn200910/16.html")
# it4 = re.finditer("<a href=\"(.*?)\" data-data=\"(.*?)\"><strong>(.*?)</strong><small>(.*?)</small></a>",page, flags=0)
# for matchObj3 in it4:
#     encryptedString = matchObj3.group(2)
#     encryptedString = encryptedString[::-1]
#     decoded = base64.b64decode(encryptedString)
#     jsonObj = json.loads(decoded)
#     if "Yun" in jsonObj["source"]:
#         print(jsonObj["source"]+ " - "+jsonObj["ids"][0])

# page = Get(langlangbayUrl + "/a/m3u8/?ref=_DqdQaHR0cHM6Ly9kb3ViYW4uZG9uZ2hvbmd6dWlkYS5jb20vMjAyMDA5MTgvOTkxMl9jNmIzMTY4NC9pbmRleC5tM3U4")
# print(page)
# matchObj4 = re.search("var m3u8url = '(.*?)'", page, flags=0)
# print(matchObj4.group(1))

