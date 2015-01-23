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
import sys
import os
from TSMApiRequest import tsmApiRequest
from TSMSpotify import *
from TSMCommon import *
dir = os.path.dirname(__file__)

def cleanstring(dirtystr):
    try:
        return str(HTMLParser.HTMLParser().unescape(dirtystr))
    except:
        return "FAIL"

def createsearchablestring(oldstr):
    return oldstr.translate(None, '@#%^&*()<>?:;{}[]-_+=\|')


def createVCPriceDict():

    currentListOfDictOfSongs = json.loads(tsmApiRequest('/v1/songs').text)['results']

    # w = open(os.path.join(dir, 'logs', 'vcLog.txt'),'w')

    db = sqlite3.connect(os.path.join(dir, 'records.sqlite'))
    c = db.cursor()

    for song in currentListOfDictOfSongs:
        spotifyURI = song['spotify_uri']
        # print "SpotifyURI: {0}".format(spotifyURI)
        songData = requestResponse(getSpotifyLookupURL(spotifyURI))
        artistID = getArtistURIFromSpotifyData(songData)
        # artistID = ""
        trackID = int(song['id'])

        # c.execute('SELECT artistid FROM ytviewcount WHERE trackid=(?)', (trackID,))
        # row = c.fetchone()
        # if(row != None):
        #     w.write("\nA Row for the Track Exists Already!")
        #     artistID = row[0]
        # else:
        #     songData = requestResponse(getSpotifyLookupURL(songURI))
        #     artistID = getArtistURIFromSpotifyData(songData)

        # w.write("\n\nNEXT TRACK:")
        # w.write("\nTrack Name/ID: {0}/{1}".format(unidecode(song['name']),trackID))
        # w.write("\nArtist Name/ID: {0}/{1}".format(unidecode(song['artist_name']),artistID))


        if song['price']==None:
            # w.write("\nNot IPO'd Yet!")
            continue

        print "Price: {0}".format(song['price'])

        try:
            searchableQuery = unidecode(song['name'] + " " + song['artist_name']).replace(" ", "%20")
        except IndexError:
            print "TODO: IndexError"
            # w.write("\nTODO: IndexError")
            continue
        # w.write("\nSearchable Query: {0}".format(searchableQuery))
        ytAPI = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=1&key=AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q&q="+searchableQuery
        while True:
            try:
                youtubeJSON = json.load(urllib2.urlopen(ytAPI))
            except urllib2.HTTPError:
                print "Connection to YT Search API Failed!"
                # w.write("\nConnection to YT Search API Failed!")
                continue
            break
        try:
            ytURI = youtubeJSON["items"][0]["id"]["videoId"]
            ytURI = ytURI.encode('ascii','ignore')
        except IndexError:
            print "YT Search API Failed to Find!"
            # w.write("\nYT Search API Failed to Find!")
            continue


        while True:
            try:
                youtubeSURL = "https://www.googleapis.com/youtube/v3/videos?id=" + ytURI + "&key=AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q&part=snippet,statistics"
                youtubeSJSON = json.load(urllib2.urlopen(youtubeSURL))
            except urllib2.HTTPError:
                print "Connection to YT Video API Failed!"
                # w.write("\nConnection to YT Video API Failed!")
                continue
            break
        try:
            viewcount = int(youtubeSJSON["items"][0]["statistics"]["viewCount"])
            numraters = int(youtubeSJSON["items"][0]["statistics"]["likeCount"])
        except IndexError:
            print "YT Video API Failed to Find!"
            # w.write("\nYT Video API Failed to Find!")
            continue

        totalVC = viewcount + numraters

        print "COMMITTING: {0}, {1}, {2}, {3}, {4}".format(trackID, artistID, spotifyURI, ytURI, totalVC)
        # w.write("\nCOMMITTING: {0}, {1}, {2}, {3}, {4}".format(trackID, artistID, spotifyURI, ytURI, totalVC))
        db.execute('INSERT OR REPLACE INTO ytviewcount VALUES (?,?,?,?,?)', (trackID, artistID, spotifyURI, ytURI, totalVC))
        db.commit()

    print "\n\nSaving Artist Averages..."
    db.execute('INSERT or REPLACE INTO artistaverages(artistid,average) SELECT artistid, AVG(viewcount) FROM ytviewcount GROUP BY artistid')
    db.commit()
    db.close()
    # w.close()


if __name__ == "__main__":
    createDB.check_database()
    print "Initializing ytviewcount Database..."
    createVCPriceDict()
    print "Success!"
