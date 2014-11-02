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
import HTMLParser
from unidecode import unidecode
import sqlite3
import createDB

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
    currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']

    db = sqlite3.connect('viewcounts.sqlite')
    c = db.cursor()

    for song in currentListOfDictOfSongs:
        spotifyURI = song['spotify_uri']
        trackID = int(song['id'])
        artistID = int(song['artist_id'])

        print "\nNEXT TRACK:"
        print "Track Name/ID: {0}/{1}".format(unidecode(song['name']),trackID)
        print "Artist Name/ID: {0}/{1}".format(unidecode(song['artist_name']),artistID)

        c.execute('SELECT trackid FROM viewcount WHERE trackid=(?)', (trackID,))
        if(c.fetchone() != None):
            print "Spotify URI Exists Already!"
            continue
        if song['price']==None:
            print "Not IPO'd Yet!"
            continue

        print "Price: {0}".format(song['price'])

        try:
            searchableQuery = unidecode(song['name'] + " " + song['artist_name']).replace(" ", "%20")
        except IndexError:
            print "TODO: WHAT?"
            continue
        print searchableQuery
        ytAPI = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=1&key=AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q&q="+searchableQuery
        while True:
            try:
                youtubeJSON = json.load(urllib2.urlopen(ytAPI))
            except urllib2.HTTPError:
                print "search failed!"
                continue
            break
        try:
            ytURI = youtubeJSON["items"][0]["id"]["videoId"]
            ytURI = ytURI.encode('ascii','ignore')
        except IndexError:
            print "Couldn't find song in YT!"
            continue


        while True:
            try:
                youtubeSURL = "https://www.googleapis.com/youtube/v3/videos?id=" + ytURI + "&key=AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q&part=snippet,statistics"
                youtubeSJSON = json.load(urllib2.urlopen(youtubeSURL))
            except urllib2.HTTPError:
                print "request failed!"
                continue
            break
        try:
            viewcount = int(youtubeSJSON["items"][0]["statistics"]["viewCount"])
            numraters = int(youtubeSJSON["items"][0]["statistics"]["likeCount"])
        except IndexError:
            print "Failed to Find!"
            continue

        totalVC = viewcount + numraters

        print "COMMITTING: {0}, {1}, {2}, {3}, {4}".format(trackID, artistID, spotifyURI, ytURI, totalVC)
        db.execute('INSERT INTO viewcount VALUES (?,?,?,?,?)', (trackID, artistID, spotifyURI, ytURI, totalVC))
        db.commit()

    db.close()


if __name__ == "__main__":
    createDB.check_database()
    createVCPriceDict()