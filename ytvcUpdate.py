#################################################
# Property of The Song Market
#
# Update csv of Last Prices.  Run this daily
#
# Created by: Matt Ao
# Sept 25th, 2014
#################################################

import json
import urllib2
import csv
import HTMLParser
from unidecode import unidecode


email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'

apiGETURL = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token

def cleanstring(dirtystr):
    try:
        return str(HTMLParser.HTMLParser().unescape(dirtystr))
    except:
        return "FAIL"

def createsearchablestring(oldstr):
    return oldstr.translate(None, '@#%^&*()<>?:;{}[]-_+=\|')


def createVCPriceDict():
    dictionaryVC = {}

    currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']

    for song in currentListOfDictOfSongs:
        while True:
            print song['name']
            print song['artist_name']
            searchableQuery = unidecode(song['name'] + " " + song['artist_name']).replace(" ", "%20")
            print searchableQuery
            ytAPI = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=1&key=AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q&q="+searchableQuery

            try:
                youtubeJSON = json.load(urllib2.urlopen(ytAPI))
                ytURI = youtubeJSON["items"][0]["id"]["videoId"]
                youtubeSURL = "https://www.googleapis.com/youtube/v3/videos?id=" + ytURI + "&key=AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q&part=snippet,statistics"
                youtubeSJSON = json.load(urllib2.urlopen(youtubeSURL))
            except urllib2.HTTPError:
                continue

            try:
                viewcount = int(youtubeSJSON["items"][0]["statistics"]["viewCount"])
                numraters = int(youtubeSJSON["items"][0]["statistics"]["likeCount"])
            except IndexError:
                print "Failed to Find!"
                continue

            totalVC = viewcount + numraters

            spotifyURI = song['spotify_uri']

            if spotifyURI in dictionaryVC:
                continue
            else:
                dictionaryVC[spotifyURI] = song['id'],ytURI,totalVC
            break

    w2 = csv.writer(open("lastVC.csv", "w+"))

    for key, val in dictionaryVC.items():
        w2.writerow([key, val])

if __name__ == "__main__":
    createVCPriceDict()