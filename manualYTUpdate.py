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
        print song['name']
        print song['artist_name']
        searchableQuery = unidecode(song['name'] + " " + song['artist_name']).replace(" ", "%20")
        print searchableQuery
        youtubeSURL = "http://gdata.youtube.com/feeds/api/videos?q=" + searchableQuery + "&orderby=viewCount&max-results=1"

        reqYT = urllib2.Request(youtubeSURL)
        responseYT = urllib2.urlopen(reqYT)
        results = responseYT.read()
        try:
            viewcount = int(results.split("viewCount='")[1].split("'",1)[0])
            numraters = int(results.split("numRaters='")[1].split("'",1)[0])
            ytURI = results.split("<id>")[2].split("</id>")[0]
        except IndexError:
            continue

        totalVC = viewcount + numraters

        spotifyURI = song['spotify_uri']

        if spotifyURI in dictionaryVC:
            continue
        else:
            dictionaryVC[spotifyURI] = [song['id'],ytURI,totalVC]

    w2 = csv.writer(open("lastVC.csv", "w+"))

    for key, val in dictionaryVC.items():
        w2.writerow([key, val])

createVCPriceDict()