#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# October 3rd, 2014
#################################################

from TSMSpotify import *
from TSMCommon import *
import requests

email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'
rawTitle = ""
rawArtist = ""
apiCREATEURL = 'http://api.thesongmarket.com/v1/songs'

def generateIPO(songURI):
    songData = requestResponse(getSpotifyLookupURL(songURI))

    global rawTitle
    rawTitle = getTitleFromSpotifyData(songData)
    cleanTitle = cleanstring(rawTitle)
    searchableTitle = createsearchablestring(cleanTitle)

    global rawArtist
    rawArtist = getArtistFromSpotifyData(songData)
    cleanArtist = cleanstring(rawArtist)
    searchableArtist = createsearchablestring(cleanArtist)

    searchableQuery = searchableTitle.replace(" ", "%20") + "%20" + searchableArtist.replace(" ", "%20")

    youtubeSURL = "http://gdata.youtube.com/feeds/api/videos?q=" + searchableQuery + "&orderby=viewCount&max-results=1"
    youtubeData = requestResponse(youtubeSURL)

    youtubeRating = float(youtubeData.split("rating average='")[1].split("'", 1)[0])/5

    numraters = int(youtubeData.split("numRaters='")[1].split("'",1)[0])
    viewcount = int(youtubeData.split("viewCount='")[1].split("'",1)[0])

    totalYTPoints = numraters + viewcount

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
    if(popularity < 0):
        popularity = 0
        price = 10

    overallPerformance = (popularity + youtubeRating)/2
    finalIPOPrice = price*overallPerformance
    return finalIPOPrice

def createIPO():
    #TODO: Grab JSON of songs next songs to IPO.  For each song, return list of IPOs?
    finalIPOPrice = generateIPO(songURI)
    print finalIPOPrice

createIPO()