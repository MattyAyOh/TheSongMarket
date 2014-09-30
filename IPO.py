#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# Sept 28th, 2014
#################################################

from TSMSpotify import *
from TSMCommon import *
import urllib2
import requests

averageDictionary = getAverageDictionary()
totalAveragePrice = getTotalAveragePrice(averageDictionary)
lastPricesDictionary = getLastPricesDictionary()

def createIPO(song):
    rawTitle = getTitleFromSpotifyData(song)
    cleanTitle = cleanstring(rawTitle)
    searchableTitle = createsearchablestring(cleanTitle)

    rawArtist = getArtistFromSpotifyData(song)
    cleanArtist = cleanstring(rawArtist)
    searchableArtist = createsearchablestring(cleanArtist)

    spotifyURI = getSpotifyURIFromSpotifyData(song)

    searchableQuery = searchableTitle.replace(" ", "%20") + "%20" + searchableArtist.replace(" ", "%20")

    spotifyURL = getSpotifySearchURL(searchableQuery)
    searchURL = "http://ws.spotify.com/search/1/track?q="+ searchableQuery
    youtubeSURL = "http://gdata.youtube.com/feeds/api/videos?q=" + searchableQuery + "&orderby=viewCount&max-results=1"

    print searchURL
    print youtubeSURL
    reqYT = urllib2.Request(youtubeSURL)
    responseYT = urllib2.urlopen(reqYT)
    results = responseYT.read()

    youtubeDURL = results.split('<entry><id>')[1].split('</id>')[0]
    print youtubeDURL
    reqDYT = urllib2.Request(youtubeDURL)
    responseDYT = urllib2.urlopen(reqYT)
    resultsDYT = responseDYT.read().split("rating average='")[1]

    rating = int(resultsDYT.split("'", 1)[0])/5
    numraters = resultsDYT.split("numRaters='")[1].split("'",1)[0]
    viewcount = resultsDYT.split("viewCount='")[1].split("'",1)[0]

    print viewcount

    spotifyRequest = urllib2.Request(searchURL)
    spotifyResponse = urllib2.urlopen(spotifyRequest).read(1400)

    album = spotifyResponse.split('<album',1)[1].split('<name>',1)[1].split('</name>',1)[0]

    popularity = float(spotifyResponse.split('<popularity>',1)[1].split('</popularity>',1)[0])
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