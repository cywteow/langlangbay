# -*- coding: utf-8 -*-
import json
import re
import sys
import base64
import urlparse
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import requests

from bs4 import BeautifulSoup
from resources.lib.database import InternalDatabase

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
imageUrl = "https://chinaq.img-ix.net/uploads/d"


xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    try:
        return base_url + '?' + urllib.urlencode(query)
    except:
        return None

def Get(url):
    headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    if req.status_code == 200:
        return req
    else:
        req = requests.get(chinaqUrl+urlparse.urlparse(url).path, headers=headers)
        req.encoding = 'utf-8'
        if req.status_code == 200:
            return req

def genList(url):
    # download pages
    InternalDatabase.connect()
    response = Get(url)
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')
    result = soup.find('ul', class_='drama_rich clearfix')
    liList = result.find_all('li', class_='sizing')
    recentUpdatedDiv = result.find_all('div', class_='txttitle')

    for item in liList:
        aTag = item.find('a')
        divTag = item.find('div', class_='title sizing')
        if chinaqUrl in aTag['href']:
            location = urlparse.urlparse(aTag['href'])
            path = location.path
        else:
            path = aTag['href']
        drama = get_drama_detail(path)
        li = xbmcgui.ListItem(drama['title'] + "("+item.find('div', class_="episode").find('a').string.encode('utf-8')+")")
        li.setArt({'poster': drama.pop('poster')})
        li.setInfo("video", drama)
        newUrl = build_url({'mode': 'genEps', 'path': path, 'domain': urlparse.urlparse(response.url).hostname})

        if newUrl is not None:
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=newUrl, listitem=li, isFolder=True)

    for div in recentUpdatedDiv:
        aTag = div.find('a')
        if chinaqUrl in aTag['href']:
            location = urlparse.urlparse(aTag['href'])
            path = location.path
        else:
            path = aTag['href']
        drama = get_drama_detail(path)
        li = xbmcgui.ListItem(aTag.string)
        li.setArt({'poster': drama.pop('poster')})
        li.setInfo("video", drama)
        newUrl = build_url({'mode': 'genEps', 'path': path, 'domain': urlparse.urlparse(response.url).hostname})

        if newUrl is not None:
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=newUrl, listitem=li, isFolder=True)
    
    InternalDatabase.close()
    xbmcplugin.endOfDirectory(addon_handle)

def genListForCountry(country):
    # download pages
    InternalDatabase.connect()
    response = Get(langlangbayUrl + "/all.html")
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')
    result = soup.find('ul', class_='drama_list').find_all('li')

    for item in result:
        if country in item['name']:
            aTag = item.find('a')
            
            if chinaqUrl in aTag['href']:
                location = urlparse.urlparse(aTag['href'])
                path = location.path
                drama = get_drama_detail(path)
                li = xbmcgui.ListItem(drama['title'])
                li.setArt({'poster': drama.pop('poster')})
                li.setInfo("video", drama)
                newUrl = build_url({'mode': 'genEps', 'path': path, 'domain': location.hostname})
            else:
                path = aTag['href']
                drama = get_drama_detail(path)
                li = xbmcgui.ListItem(drama['title'])
                li.setArt({'poster': drama.pop('poster')})
                li.setInfo("video", drama)
                newUrl = build_url({'mode': 'genEps', 'path': path, 'domain': urlparse.urlparse(response.url).hostname})
            
            if newUrl is not None:
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=newUrl, listitem=li, isFolder=True)

    InternalDatabase.close()
    xbmcplugin.endOfDirectory(addon_handle)

def playUrl(video_url):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    li = xbmcgui.ListItem(path=video_url)
    li.setInfo( type="video", infoLabels={ "Path" : video_url } )
    playlist.add(url=video_url, listitem=li)
    xbmc.Player().play(playlist)

def playResolvedUrl(url):
    li = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(addon_handle, True, li)

def getDescription(document):
    plot = ""
    try:
        description = document.find('div', class_="description")
        for element in description.contents:
            if element.name == "font":
                plot = plot[:-1]
                plot += element.string.strip() + "\n"
            elif element.name != "br":
                plot += element.strip() + "\n"
    except:
        plot = "Error Reading Description"
    return plot

def get_drama_detail(path):
    drama = InternalDatabase.fetchone(path)

    if drama is None:
        response = Get(chinaqUrl+path)
        response.encoding = 'utf-8'
        document = BeautifulSoup(response.text, 'html.parser')
        h1 = document.find('div', id='contain').find('h1')
        title = h1.contents[0][:-3].strip()
        img = imageUrl+path[:-1]+".jpg"
        plot = getDescription(document)

        InternalDatabase.add((path,
                              img,
                              title,
                              plot))
        drama = InternalDatabase.fetchone(path)

    return drama


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
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')
    aTag = soup.find('div', class_="items sizing").find_all('a')

    for item in aTag:
        if item.has_attr('onclick'):
            pattern = "xxx\(\'(.*?)\',\'(.*?)\',(.*?)\);return false;"
            result = re.search(pattern, item['onclick'], flags=0)
            path = newUrl + result.group(2) + ".html"
        elif args['path'][0] in item['href']:
            path = "https://" + args['domain'][0] + item['href']
        else:
            path = newUrl + item['href']

        title = item.string
        li = xbmcgui.ListItem(title)
        li.setInfo("video", {"title": title})
        li.setProperty('IsPlayable', 'true')
        url = build_url({'mode': 'genSources', 'path': path})
        if url is not None:
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(addon_handle)

#Listing of video sources
elif mode[0] == 'genSources':
    #eg. path = https://langlangbay.org/cn200827/4.html
    sourceList = []
    newUrl = urllib.unquote(args['path'][0])
    response = Get(newUrl)
    page = response.text
    
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
        newPage = response.text
        result = re.search("var m3u8url = '(.*?)'", newPage, flags=0)
        # playUrl(urllib.unquote(urllib.unquote(result.group(1))))
        playResolvedUrl(urllib.unquote(urllib.unquote(result.group(1))))

elif mode[0] == 'm3u8':
    playUrl(urllib.unquote(urllib.unquote(args['path'][0])))

else:
    xbmcgui.Dialog().ok(u'is developing'.encode('utf-8'),args['path'][0].encode('utf-8'))
    print ('unsupport link => ' + args['path'][0].encode('utf-8'))


