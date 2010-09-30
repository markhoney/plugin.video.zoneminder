import urllib
import urllib2
import re
import xbmcplugin
import xbmcgui

#ZoneMinder Plugin

#plugin constants
__plugin__ = "ZoneMinder"
__author__ = "tim-"
__url__ = "http://www.losingcable.com/XBMC/zm/"
__credits__ = "Voinage - Thanks for the tutorial"
__version__ = "0.2.1"

#__settings__ = xbmcaddon.Addon(id='plugin.video.zoneminder')
#__scriptID__      = "plugin.video.zoneminder"

__pluginhandle__ = int(sys.argv[1])
                       
def LISTMONITORS(url):
        ## for authentication i will need to hit a few URLs I am guessing. login then hit plain index and see if it works
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile("zmWatch(.+?)\'.+?;\">(.+?)</a>").findall(link)
        if len(match)==0:
                print "either no cameras or auth failed"
        for url,name in match:
                thumbnail="camera.png"
                if xbmcplugin.getSetting(__pluginhandle__, "reqauth")=="true":
                        newurl="http://" + xbmcplugin.getSetting(__pluginhandle__, "ZM_URL") + "/cgi-bin/nph-zms?mode=mpeg&monitor=" + url + "&scale=100&bitrate=" + xbmcplugin.getSetting(__pluginhandle__, "bitrate") + "&maxfps=" + xbmcplugin.getSetting(__pluginhandle__, "fps") + "&format=asf&user=" + xbmcplugin.getSetting(__pluginhandle__, "username") + "&pass=" + xbmcplugin.getSetting(__pluginhandle__, "password")
                else:
                        newurl="http://" + xbmcplugin.getSetting(__pluginhandle__, "ZM_URL") + "/cgi-bin/nph-zms?mode=mpeg&monitor=" + url + "&scale=100&bitrate=" + xbmcplugin.getSetting(__pluginhandle__, "bitrate") + "&maxfps=" + xbmcplugin.getSetting(__pluginhandle__, "fps") + "&format=asf"
                print newurl
                addLink(name,newurl,thumbnail)

     

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
if len(sys.argv) >= 3:
        params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


#Check if authentication is required and build the main page URL as needed
if xbmcplugin.getSetting(__pluginhandle__, "reqauth")=="true":
        zurl = "http://" + xbmcplugin.getSetting(__pluginhandle__, "ZM_URL") + "/zm/index.php?username=" + xbmcplugin.getSetting(__pluginhandle__, "username") + "&password=" + xbmcplugin.getSetting(__pluginhandle__, "password") + "&action=login"
else:
        zurl = "http://" + xbmcplugin.getSetting(__pluginhandle__, "ZM_URL") + "/zm"
               
#print xbmcplugin.getSetting("reqauth") + "  --  " + zurl
LISTMONITORS(zurl)
        




xbmcplugin.endOfDirectory(int(sys.argv[1]))












