#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# Sept 28th, 2014
#################################################

from TSMSpotify import *
from TSMCommon import *
import requests

averageDictionary = getAverageDictionary()
totalAveragePrice = getTotalAveragePrice(averageDictionary)
lastPricesDictionary = getLastPricesDictionary()

def createIPO(songURI):
    songData = requestResponse(getSpotifyLookupURL(songURI))

    rawTitle = getTitleFromSpotifyData(songData)
    cleanTitle = cleanstring(rawTitle)
    searchableTitle = createsearchablestring(cleanTitle)

    rawArtist = getArtistFromSpotifyData(songData)
    cleanArtist = cleanstring(rawArtist)
    searchableArtist = createsearchablestring(cleanArtist)

    searchableQuery = searchableTitle.replace(" ", "%20") + "%20" + searchableArtist.replace(" ", "%20")

    youtubeSURL = "http://gdata.youtube.com/feeds/api/videos?q=" + searchableQuery + "&orderby=viewCount&max-results=1"
    youtubeData = requestResponse(youtubeSURL)

    youtubeRating = float(youtubeData.split("rating average='")[1].split("'", 1)[0])/5

    numraters = youtubeData.split("numRaters='")[1].split("'",1)[0]
    viewcount = youtubeData.split("viewCount='")[1].split("'",1)[0]

    album = getAlbumFromSpotifyData(songData)
    popularity = getPopularityFromSpotifyData(songData)
    scaledpopularity = (popularity-.70)/.30
    if(scaledpopularity < 0):
        scaledpopularity = 0
        price = 10

    print price

    market = "Mainstream"

    #################################################
    # Grab all Songs (Later by Artist)
    # Search if current song exists in Song table
    #################################################

    foundFlag = False
    oldPrice = 0
    songID = 0
    for result in currentListOfDictOfSongs:
        if result['spotify_uri'] == spotifyURI:
            print 'FOUND IT!'
            resultAvgPrice = int(averageDictionary[cleanstring(result['artist_name'])])
            if price < resultAvgPrice:
                price = (resultAvgPrice+price)/2
            oldPrice = result['price']
            foundFlag = True;
            songID = result['id']
            break

    #################################################
    # Populate database
    #################################################
    change = 0
    body = { 'user_email':email, 'user_token':token, 'song[name]':rawTitle, 'song[artist_name]':rawArtist, 'song[price]':price, 'song[ipo_value]':price, 'song[change]':change }

    if (foundFlag):
        change = price - oldPrice
        apiCREATEURL += '/' + str(songID)
        p = requests.put(apiCREATEURL, data=body)
        print "PUT!"

    else:
        # p = requests.post(apiPOSTURL, data=body)
        # print p.status_code
        # print p.text
        continue