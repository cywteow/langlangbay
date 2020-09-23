
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
arabUrl = "https://arabnewsworld.com"

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def Get(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    return urllib2.urlopen(req).read()

def genList(url):
    # download pages
    page = Get(url)
    # init regex search
    it = re.finditer("<a href=\"(.*?)\">\n\t\t\t\t\t\t<div class=\"title sizing\">(.*?)</div>", page, flags=0)
    it2 = re.finditer("<div class=\"txttitle\">\n\t\t\t\t<a href=\"(.*?)\">(.*?)\(.*?\)</a>", page, flags=0)
    # add to list
    for matchObj in it:
        try:
            li = xbmcgui.ListItem(matchObj.group(2))
            url = build_url({'mode': 'video-info', 'path': matchObj.group(1)})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        except BaseException:
            print("err")
    for matchObj in it2:
        try:
            li = xbmcgui.ListItem(matchObj.group(2))
            url = build_url({'mode': 'video-info', 'path': matchObj.group(1)})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        except BaseException:
            print("err")

    xbmcplugin.endOfDirectory(addon_handle)

def genListForCountry(country):
    # download pages
    page = Get(langlangbayUrl + "/all.html")

    pattern = "<li name=\"all"+country+"(.*?)\"><a href=\"(.*?)\">(.*?)</a></li>"
    # init regex search
    it = re.finditer(pattern, page, flags=0)
    # add to list
    for matchObj in it:
        li = xbmcgui.ListItem(matchObj.group(3))
        path = matchObj.group(2)
        if chinaqUrl in path:
            result = re.search(chinaqUrl+"(.*?$)", path, flags=0)
            if result:
                url = build_url({'mode': 'video-info-all', 'path': result.group(1)})
        else:
            url = build_url({'mode': 'video-info', 'path': matchObj.group(2)})

        if url:
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        print("err")

    xbmcplugin.endOfDirectory(addon_handle)

# decode
def ttdecode(code):
    # print code
    str = ""
    key = "ttrandomkeyqdramanet"
    for i in range(0,len(code)):
        if (0 == i or 0 == i % (len(key) + 1)):
            str += code[i]

    return str[::-1]

def playUrl(video_url):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    li = xbmcgui.ListItem(path=video_url)
    li.setInfo( type="video", infoLabels={ "Path" : video_url } )
    playlist.add(url=video_url, listitem=li)
    xbmc.Player().play(playlist)

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

elif mode[0] == 'K-List':
    genList(langlangbayUrl + "/kr/")

elif mode[0] == 'J-List':
    genList(langlangbayUrl + "/jp/")

elif mode[0] == 'C-List':
    genList(langlangbayUrl + "/cn/")

elif mode[0] == 'T-List':
    genList(langlangbayUrl + "/tw/")

#Listing of video eps
elif mode[0] == 'video-info':
    #eg. path = /cn200827/
    
    # download pages
    try:
        newUrl = arabUrl + args['path'][0]
        page = Get(newUrl)
    except:
        newUrl = chinaqUrl + args['path'][0]
        page = Get(newUrl)
    # init regex search
    count = 0
    it = re.finditer("<li class=\"sizing\"><h2><a rel=\"nofollow noopener noreferrer\" onclick=\"xxx\('(.*?)','(.*?)',(.*)>(.*?)</a>", page, flags=0)

    # add to list
    for matchObj in it:
        li = xbmcgui.ListItem(matchObj.group(4))
        path = newUrl + matchObj.group(2) + ".html"
        # print("path to video-list is "+ path)
        url = build_url({'mode': 'video-list', 'path': path})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        count += 1

    if(count == 0):
        it = re.finditer("<li class=\"sizing\"><h2><a href=\"(.*?).html\">(.*?)</a></h2></li>", page, flags=0)
        for matchObj in it:
            li = xbmcgui.ListItem(matchObj.group(2))
            path = newUrl + matchObj.group(1) + ".html"
            # print("path to video-list is "+ path)
            url = build_url({'mode': 'video-list', 'path': path})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

#Listing of video eps
elif mode[0] == 'video-info-all':
    #eg. path = /cn200827/
    newUrl = chinaqUrl + args['path'][0]
    # download pages
    page = Get(newUrl)
    # init regex search
    count = 0
    it = re.finditer("<li class=\"sizing\"><h2><a rel=\"nofollow noopener noreferrer\" onclick=\"xxx\('(.*?)','(.*?)',(.*)>(.*?)</a>", page, flags=0)

    # add to list
    for matchObj in it:
        li = xbmcgui.ListItem(matchObj.group(4))
        path = chinaqUrl + matchObj.group(2) + ".html"
        # print("path to video-list is "+ path)
        url = build_url({'mode': 'video-list', 'path': path})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        count += 1

    if(count == 0):
        it = re.finditer("<li class=\"sizing\"><h2><a href=\"(.*?).html\">(.*?)</a></h2></li>", page, flags=0)
        for matchObj in it:
            li = xbmcgui.ListItem(matchObj.group(2))
            if args['path'][0] in matchObj.group(1):
                path = chinaqUrl + matchObj.group(1) + ".html"
            else:
                path = chinaqUrl + args['path'][0] + matchObj.group(1) + ".html"
            # print("path to video-list is "+ path)
            url = build_url({'mode': 'video-list', 'path': path})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

#Listing of video sources
elif mode[0] == 'video-list':
    # print("path in video-list is " + args['path'][0])
    #eg. path = https://langlangbay.org/cn200827/4.html
    # download pages
    newUrl = urllib.unquote(args['path'][0])
    # print(newUrl)
    page = Get(newUrl)
    sourceList = []
    # init regex search
    it = re.finditer("<a href=\"(.*?)\" data-data=\"(.*?)\"><strong>(.*?)</strong><small>(.*?)</small></a>", page, flags=0)

    # add to list
    for matchObj in it:
        encryptedString = matchObj.group(2)
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
            # url = build_url({'mode': source, 'path': "/a/m3u8/", 'ref': ref})
            # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    
    index = xbmcgui.Dialog().select("Choose Source", sourceList)

    if index != -1:
        newPage = Get(langlangbayUrl + "/a/m3u8/?ref=" + sourceList[index].getProperty("ref"))
        result = re.search("var m3u8url = '(.*?)'", newPage, flags=0)
        playUrl(urllib.unquote(urllib.unquote(result.group(1))))

    # xbmcplugin.endOfDirectory(addon_handle)

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
