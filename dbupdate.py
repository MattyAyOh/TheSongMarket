#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# July 19th, 2014
#################################################

import json
from IPO import *
import csv

spotifyAPIURL = 'http://ws.spotify.com/search/1/track?q=genre:pop'
apiPOSTURL = 'http://api.thesongmarket.com/v1/songs'
apiGETURL = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token
apiCREATEURL = 'http://api.thesongmarket.com/v1/songs'

def getsongslistfromspotifydata():
    spotifyRequest = urllib2.Request(spotifyAPIURL)
    spotifyResponse = urllib2.urlopen(spotifyRequest)
    spotifyData = spotifyResponse.read()
    return spotifyData.split('<track ')[1:]

# Helper Functions:
def cleanstring(dirtystr):
    return str(HTMLParser.HTMLParser().unescape(dirtystr))


def createsearchablestring(oldstr):
    return oldstr.translate(None, '@#%^&*()<>?:;{}[]-_+=\|')

def getAveragePrice():
    totalPrice = 0
    songCount = 0
    for songDict in currentListOfDictOfSongs:
        totalPrice += int(songDict['price'])
        songCount += 1
    return totalPrice/songCount

def getAverageDictionary():
    tempDict = {}
    for key, val in csv.reader(open("averages.csv")):
        tempDict[key] = val
    return tempDict

def getLastPricesDictionary():
    tempDict = {}
    for key, val in csv.reader(open("lastPrices.csv")):
        tempDict[key] = val
    return tempDict

# Main Script:

currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']
songsList = getsongslistfromspotifydata()
averagePrice = getAveragePrice()
averageDictionary = getAverageDictionary()
lastPricesDictionary = getLastPricesDictionary()

for song in songsList:

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

    album = getAlbumFromSpotifyData(song)
    popularity = getPopularityFromSpotifyData(song)
    if(popularity < 0):
        popularity = 0
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
        createIPO(spotifyURI)
        continue
