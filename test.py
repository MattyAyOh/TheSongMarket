import json
import urllib2
# ytAPI = "https://www.googleapis.com/youtube/v3/search?q=sum 41 in too deep&key=&part=snippet,statistics"
ytAPI = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=1&key=AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q&q=blink"
youtubeJSON = json.load(urllib2.urlopen(ytAPI))
print youtubeJSON["items"]
published = youtubeJSON["items"][0]["id"]["videoId"]
# viewCount = youtubeJSON["items"][0]["statistics"]["viewCount"]
print published
# print viewCount
# import requests
# email = 'mattyayoh@gmail.com'
# token = 'PQBTwrEmyRJrR8GMs6ij'
#
# CurrentVC = 210794
# LastVC = 205922
# differenceVC = CurrentVC - LastVC
# print differenceVC
# print CurrentVC
# performancePercent = float(float(differenceVC)/float(CurrentVC))
#
# print performancePercent
#
# expectedPercent= .01
# change = float(pow(performancePercent,2)/pow(expectedPercent,2)*10)
# print change
#
# body = {'user_email': email, 'user_token': token, 'song[price]': 110}
# headers = {'content-type': 'application/x-www-form-urlencoded'}
#
# apiUPDATEURL = 'http://api.thesongmarket.com/v1/songs/2601'
# p = requests.put(apiUPDATEURL, data=body, headers=headers)


# from IPO import *
# from ytvcUpdate import *
#
# apiPOSTURL = 'http://api.thesongmarket.com/v1/songs'
# apiGETURL = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token
#
# #################################################
# # Main Script
# #################################################
#
# if(not(os.path.isfile('lastVC.csv'))):
#     createVCPriceDict()
#
# currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']
# lastVCDictionary = getLastVCDictionary()
#
# for song in currentListOfDictOfSongs:
#     spotifyURI = song['spotify_uri']
#
#     try:
#         currentPrice = int(song['price'])
#     except TypeError:
#         # print "No IPO Yet!"
#         continue
#
#     try:
#         print lastVCDictionary[spotifyURI]
#         lastVC = int(lastVCDictionary[spotifyURI][2].replace(']','').replace(' ',''))
#         youtubeURI = lastVCDictionary[spotifyURI][1][-12:-1]
#     except KeyError:
#         print "Song not found in last VC CSV!"
#         continue
#
#     songID = song['id']
#
#     rawTitle = song['name']
#     cleanTitle = cleanstring(rawTitle)
#     if cleanTitle == "FAIL":
#         print "Dirty Title"
#         print rawTitle
#         continue
#     searchableTitle = createsearchablestring(cleanTitle)
#
#     rawArtist = song['artist_name']
#     cleanArtist = cleanstring(rawArtist)
#     if cleanArtist == "FAIL":
#         print "Dirty Artist"
#         print rawArtist
#         continue
#     searchableArtist = createsearchablestring(cleanArtist)
#
#
#     searchableQuery = searchableTitle.replace(" ", "%20") + "%20" + searchableArtist.replace(" ", "%20")
#     # deprecated
#     # youtubeSURL = "http://gdata.youtube.com/feeds/api/videos?q=" + searchableQuery + "&orderby=viewCount&max-results=1"
#     youtubeSURL = "https://www.googleapis.com/youtube/v3/videos?id=" + youtubeURI + "&key=AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q&part=snippet,statistics"
#
#     print youtubeSURL