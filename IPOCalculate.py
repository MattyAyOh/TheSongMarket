from TSMSpotify import *
from TSMCommon import *
import sys
import os
import sqlite3

def generateIPO(songURI):
    songData = requestResponse(getSpotifyLookupURL(songURI))

    rawTitle = getTitleFromSpotifyData(songData)
    cleanTitle = cleanstring(rawTitle)
    searchableTitle = createsearchablestring(cleanTitle)

    rawArtist = getArtistFromSpotifyData(songData)
    cleanArtist = cleanstring(rawArtist)
    searchableArtist = createsearchablestring(cleanArtist)

    searchableQuery = searchableTitle.replace(" ", "%20") + "%20" + searchableArtist.replace(" ", "%20")

    youtubeSURL = "http://gdata.youtube.com/feeds/api/videos?q=" + searchableQuery + "&max-results=1"
    youtubeData = requestResponse(youtubeSURL)

    published = youtubeData.split("<published>")[1].split("</published>")[0]
    publishedDate = getDateUtilFromString(published)

    currentDate = datetime.datetime.now()
    differenceInDate = (currentDate - publishedDate).days

    scale = 1

    if(differenceInDate < 14):
        scale += (5*((14-differenceInDate)/14))

    youtubeRating = float(youtubeData.split("rating average='")[1].split("'", 1)[0])/5

    numraters = int(youtubeData.split("numRaters='")[1].split("'",1)[0])
    viewcount = int(youtubeData.split("viewCount='")[1].split("'",1)[0])
    totalYTPoints = numraters + viewcount

    totalYTPoints *= scale

    artistURI = getArtistURIFromSpotifyData(songData)
    dir = os.path.dirname(__file__)
    db = sqlite3.connect(os.path.join(dir, 'records.sqlite'))
    c = db.cursor()
    c.execute('SELECT average FROM artistaverages WHERE artistid=(?)', (artistURI,))
    row = c.fetchone()

    artistAvgPoints = 0
    if(row != None):
        artistAvgPoints = row[0]
    if totalYTPoints < artistAvgPoints:
        totalYTPoints = (artistAvgPoints+totalYTPoints)/2

    price = 0
    if totalYTPoints <= 1000: #1K Bracket
        price = 10

    elif totalYTPoints > 1000 and totalYTPoints <= 10000: #10K Bracket
        price = (((totalYTPoints-1000.0)/9000.0)*40)+10
    elif totalYTPoints > 10000 and totalYTPoints <= 100000: #100K Bracket
        price = (((totalYTPoints-10000.0)/90000.0)*50)+50
    elif totalYTPoints > 100000 and totalYTPoints <= 1000000: #1 Milo Bracket
        price = (((totalYTPoints-100000.0)/900000.0)*400)+100
    elif totalYTPoints > 1000000 and totalYTPoints <= 10000000: #10 Milo Bracket
        price = (((totalYTPoints-1000000.0)/9000000.0)*500)+500
    elif totalYTPoints > 10000000 and totalYTPoints <= 100000000: #100 Milo Bracket
        price = (((totalYTPoints-10000000.0)/90000000.0)*4000)+1000
    elif totalYTPoints > 100000000: #1 Bilo Bracket
        price = (((totalYTPoints-100000000.0)/900000000.0)*5000)+5000

    popularity = getPopularityFromSpotifyData(songData)

    overallPerformance = (popularity + youtubeRating)/2
    finalIPOPrice = price*overallPerformance

    return finalIPOPrice


if __name__ == '__main__':
  listofArgs = sys.argv[1:]
  if len(listofArgs) == 1:
    spotifyURI = listofArgs[0]
    IPOPrice = generateIPO(spotifyURI)
    print IPOPrice
  else:
    print "ERROR: Missing Spotify URI argument"
