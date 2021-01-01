# -*- coding: utf-8 -*-
import json
import re
import sys

import base64
from urllib.parse import urlparse, urlencode, unquote, parse_qs


# def Get(url):
#     req = urllib2.Request(url)
#     req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
#     response = urllib2.urlopen(req)
#     return response

langlangbayUrl = "https://langlangbay.org"

base_url = 'plugin://plugin.video.langlangbay/'

print('plugin://plugin.video.langlangbay/' + '?' +urlencode({'mode': 'C-List'}))




# soup = BeautifulSoup(Get("https://www2.gogoanime.video/burn-the-witch-episode-3").read(), 'html.parser')

# f = open("test.html", "w")
# f.write(soup.prettify("utf-8"))
# f.close()
    # if element.encode('utf-8') != "<br/>" || :
    #     plot += element.encode('utf-8')

# for item in aTag:
    # pattern = "xxx\(\'(.*?)\',\'(.*?)\',(.*?)\);return false;"
    # if item.has_attr('onclick'):
    #     onclick = item['onclick']
    #     result = re.search(pattern, onclick, flags=0)
    #     title = item.string.encode('utf-8')
    #     print(result.group(2))
    #     print(title)
    # print(item['data-data'])
    

# result = soup.find('ul', class_='drama_rich clearfix').find_all('div', class_='txttitle')

# for div in result:
#     result2 = div.find('a')
#     print(result2['href'])

# print(soup.prettify('utf-8'))

# path = "test"

# page = Get(langlangbayUrl + "/cn/")
# it = re.finditer("<a href=\"(.*?)\">\n\t\t\t\t\t\t<div class=\"title sizing\">(.*?)</div>", page, flags=0)
# it2 = re.finditer("<div class=\"txttitle\">\n\t\t\t\t<a href=\"(.*?)\">(.*?)\(.*?\)</a>", page, flags=0)
# for matchObj in it2:
#     path = matchObj.group(1)
#     break

# print(settings['langlangbay']['url'])

# page2 = Get(settings['langlangbay']['url'] + "/cn200913/")
# it3 = re.finditer("<li class=\"sizing\"><h2><a rel=\"nofollow noopener noreferrer\" onclick=\"xxx\('(.*?)','(.*?)',(.*)>(.*?)</a>", page2, flags=0)
# matchObj2 = None
# for matchObj2 in it3:
#     print('test')
#     print(matchObj2.group(4)+", "+matchObj2.group(2))
# if(matchObj2 is None):
#     it3 = re.finditer("<li class=\"sizing\"><h2><a href=\"(.*?).html\">(.*?)</a></h2></li>",page2,flags=0)
#     for matchObj2 in it3:
#         print('test2')
#         print(matchObj2.group(2) + " - " + matchObj2.group(1))

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

# encryptedString = "=0XXiQTVz0Ed1MUZsJVbiBXO55kbKFDZUZ1VkxWOp10dJRVT0UERNlHOTJmdO1GToJ1VhFDczIGao1GTolzVZ9WO5xkNNh0YwIFShFFZxR0XiwiI0U1MNRXNDVGbS1mYwlzQjJjSU1kVShkTElzUPdXSU10MFRUT5hzUiZnTtxUNGdkWwZlblFTVqxEcshVY1kTeMZTTINGMShUYRRWcE9lIbpjIzRWaiwiIuVXWaJiOiU2YyV3bzJye"
# encryptedString = encryptedString[::-1]
# decoded = base64.b64decode(encryptedString)
# print(decoded)