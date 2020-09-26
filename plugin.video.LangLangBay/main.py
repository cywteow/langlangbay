
# import ptvsd
# ptvsd.enable_attach(secret = '1')
# ptvsd.wait_for_attach


# -*- coding: utf-8 -*-
import json
import re
import sys
import urllib
import base64

import urllib2
import urlparse
import xbmc
import xbmcgui
import xbmcplugin

from pprint import pprint
from bs4 import BeautifulSoup

#init plugin
print("sys.argv is ")
print(sys.argv)
base_url = sys.argv[0]
# print("BaseUrl is "+ base_url)
addon_handle = int(sys.argv[1])
# print("addon_handle is "+ sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
print("args is ")
print(args)

langlangbayUrl = "https://langlangbay.org"
chinaqUrl = "https://chinaq.tv"

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def Get(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    return urllib2.urlopen(req)

def genList(url):
    # download pages
    response = Get(url)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    result = soup.find('ul', class_='drama_rich clearfix')
    liList = result.find_all('li', class_='sizing')
    recentUpdatedDiv = result.find_all('div', class_='txttitle')

    for item in liList:
        aTag = item.find('a')
        divTag = item.find('div', class_='title sizing')
        li = xbmcgui.ListItem(divTag.string.encode('utf-8'))
        newUrl = build_url({'mode': 'genEps', 'path': aTag['href'], 'domain': urlparse.urlparse(response.geturl()).hostname})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=newUrl, listitem=li, isFolder=True)

    for div in recentUpdatedDiv:
        aTag = div.find('a')
        li = xbmcgui.ListItem(re.search("(.+)\(.*\)", aTag.string.encode('utf-8'), flags=0).group(1))
        newUrl = build_url({'mode': 'genEps', 'path': aTag['href'], 'domain': urlparse.urlparse(response.geturl()).hostname})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=newUrl, listitem=li, isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)

def genListForCountry(country):
    # download pages
    response = Get(langlangbayUrl + "/all.html")
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    result = soup.find('ul', class_='drama_list').find_all('li')

    for item in result:
        if country in item['name']:
            aTag = item.find('a')
            li = xbmcgui.ListItem(aTag.string.encode('utf-8'))
            if chinaqUrl in aTag['href']:
                location = urlparse.urlparse(aTag['href'].encode('utf-8'))
                newUrl = build_url({'mode': 'genEps', 'path': location.path, 'domain': location.hostname})
            else:
                newUrl = build_url({'mode': 'genEps', 'path': aTag['href'], 'domain': urlparse.urlparse(response.geturl()).hostname})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=newUrl, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

def playUrl(video_url):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    li = xbmcgui.ListItem(path=video_url)
    li.setInfo( type="video", infoLabels={ "Path" : video_url } )
    playlist.add(url=video_url, listitem=li)
    xbmc.Player().play(playlist)

def getDescription(page):
    plot = ""
    try:
        soul = BeautifulSoup(page, 'html.parser')
        description = soup.find('div', class_="description")
        for element in description.contents:
            if element.name == "font":
                plot = plot[:-1]
                plot += element.string.encode('utf-8').strip() + "\n"
            elif element.name != "br":
                plot += element.encode('utf-8').strip() + "\n"
    except:
        plot = "Error Reading Description"
    return plot


# home page
mode = args.get('mode', None)
if mode is None:
    # li = xbmcgui.ListItem(u'List'.encode('utf-8'))
    # url = build_url({'mode': 'List'})
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    li = xbmcgui.ListItem(u'Recent Jp'.encode('utf-8'))
    url = build_url({'mode': 'J-List'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    li = xbmcgui.ListItem(u'Recent Kr'.encode('utf-8'))
    url = build_url({'mode': 'K-List'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    li = xbmcgui.ListItem(u'Recent CN'.encode('utf-8'))
    url = build_url({'mode': 'C-List'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    li = xbmcgui.ListItem(u'Recent TW'.encode('utf-8'))
    url = build_url({'mode': 'T-List'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    li = xbmcgui.ListItem(u'All Jp'.encode('utf-8'))
    url = build_url({'mode': 'All Jp'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    li = xbmcgui.ListItem(u'All Kr'.encode('utf-8'))
    url = build_url({'mode': 'All Kr'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    li = xbmcgui.ListItem(u'All Cn'.encode('utf-8'))
    url = build_url({'mode': 'All Cn'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    li = xbmcgui.ListItem(u'All Tw'.encode('utf-8'))
    url = build_url({'mode': 'All Tw'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    li = xbmcgui.ListItem(u'All Hk'.encode('utf-8'))
    url = build_url({'mode': 'All Hk'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)



    # li = xbmcgui.ListItem(u'Search'.encode('utf-8'))
    # url = build_url({'mode': 'Search'})
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # li = xbmcgui.ListItem(u'Test'.encode('utf-8'))
    # url = build_url({'mode': 'Test'})
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'Recently update':
    genList(langlangbayUrl + "/update.html")

elif mode[0] == 'All Jp':
    genListForCountry("jp")

elif mode[0] == 'All Kr':
    genListForCountry("kr")

elif mode[0] == 'All Cn':
    genListForCountry("cn")

elif mode[0] == 'All Tw':
    genListForCountry("tw")

elif mode[0] == 'All Hk':
    genList(langlangbayUrl + "/hk/")

elif mode[0] == 'K-List':
    genList(langlangbayUrl + "/kr/")

elif mode[0] == 'J-List':
    genList(langlangbayUrl + "/jp/")

elif mode[0] == 'C-List':
    genList(langlangbayUrl + "/cn/")

elif mode[0] == 'T-List':
    genList(langlangbayUrl + "/tw/")

#Listing of video eps
elif mode[0] == 'genEps':
    #eg. path = /cn200827/
    newUrl = "https://" + args['domain'][0] + args['path'][0]
    response = Get(newUrl)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    aTag = soup.find('div', class_="items sizing").find_all('a')
    plot = getDescription(page)

    for item in aTag:
        if item.has_attr('onclick'):
            pattern = "xxx\(\'(.*?)\',\'(.*?)\',(.*?)\);return false;"
            result = re.search(pattern, item['onclick'], flags=0)
            path = newUrl + result.group(2) + ".html"
        elif args['path'][0] in item['href']:
            path = "https://" + args['domain'][0] + item['href']
        else:
            path = newUrl + item['href']

        title = item.string.encode('utf-8')
        li = xbmcgui.ListItem(title)
        li.setInfo("video", {"plot": plot})
        url = build_url({'mode': 'genSources', 'path': path})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

#Listing of video sources
elif mode[0] == 'genSources':
    #eg. path = https://langlangbay.org/cn200827/4.html
    sourceList = []
    newUrl = urllib.unquote(args['path'][0])
    response = Get(newUrl)
    page = response.read()
    
    soup = BeautifulSoup(page, 'html.parser')
    aTag = soup.find('div', class_="sources").find_all('a')

    for item in aTag:
        encryptedString = item['data-data']
        encryptedString = encryptedString[::-1]
        decoded = base64.b64decode(encryptedString)
        jsonObj = json.loads(decoded)
        source = jsonObj["source"]
        ref = jsonObj["ids"]
        if "Yun" in source:
            if len(ref) > 1:
                count = 1
                for refItem in ref:
                    li = xbmcgui.ListItem(source+" Part "+ str(count))
                    li.setProperty("ref", refItem)
                    sourceList.append(li)
                    count += 1
            else:
                li = xbmcgui.ListItem(source)
                li.setProperty("ref", ref[0])
                sourceList.append(li)
    
    index = xbmcgui.Dialog().select("Choose Source", sourceList)

    if index != -1:
        response = Get("https://" + urlparse.urlparse(newUrl).hostname + "/a/m3u8/?ref=" + sourceList[index].getProperty("ref"))
        newPage = response.read()
        result = re.search("var m3u8url = '(.*?)'", newPage, flags=0)
        playUrl(urllib.unquote(urllib.unquote(result.group(1))))

elif mode[0] == 'dailymotion':
    playUrl("plugin://plugin.video.dailymotion_com/?mode=playVideo&url=" + args['path'][0])

elif mode[0] == 'youtube':
    playUrl("plugin://plugin.video.youtube/play/?video_id=" + args['path'][0])

elif mode[0] == 'm3u8':
    playUrl(urllib.unquote(urllib.unquote(args['path'][0])))
    
elif mode[0] == 'rapidvideo':
    # download pages
    page = Get('https://www.rapidvideo.com/e/' + args['path'][0] + '&q=720p')
    # init regex search
    matchObj = re.search("src=\"(https:\/\/.*?mp4)\"", page, flags=0)
    # get video url
    playUrl(matchObj.group(1))

else:
    xbmcgui.Dialog().ok(u'is developing'.encode('utf-8'),args['path'][0].encode('utf-8'))
    print ('unsupport link => ' + args['path'][0].encode('utf-8'))
