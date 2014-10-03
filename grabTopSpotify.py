#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# July 19th, 2014
#################################################

import json
from IPO import *

apiPOSTURL = 'http://api.thesongmarket.com/v1/songs'
apiGETURL = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token

#################################################
# Main Script
#################################################

currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']
songsList = getListofSongsFromSpotifyData()
averagePrice = getTotalAveragePrice()
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

    apiCHANGEURL = 'http://api.thesongmarket.com/v1/songs/'+str(songID)+'/song_changes'

    if (foundFlag):
        change = price - oldPrice
        apiCREATEURL += '/' + str(songID)
        p = requests.post(apiCREATEURL, data=body)
        print "PUT!"

    else:
        createIPO(spotifyURI)
        continue
