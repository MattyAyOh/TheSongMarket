#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# July 19th, 2014
#################################################

import json
from IPO import *
from ytvcUpdate import *

apiPOSTURL = 'http://api.thesongmarket.com/v1/songs'
apiGETURL = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token

#################################################
# Main Script
#################################################

if(not(os.path.isfile('lastPrices.csv')) or not(os.path.isfile('lastVC.csv'))):
    createVCPriceDict()

currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']
spotifyTopSongsList = getListofSongsFromSpotifyData()
averagePrice = getTotalAveragePrice()
averageDictionary = getAverageDictionary()
lastPricesDictionary = getLastPricesDictionary()

for song in spotifyTopSongsList:

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

    resultsYT = responseDYT.read()

    publishedDate = getDateUtilFromString(results.YT.split("<published>")[1].split("</published>")[0])
    currentDate = datetime.datetime.now()
    differenceInDate = (currentDate - publishedDate).days

    expectedPercent = .01
    if( differenceInDate > 90 ):
        daysExpired = differenceInDate - 90
        monthsExpired = int(daysExpired/30)
        if monthsExpired >= 45:
            expectedPercent = .001
        else:
            expectedPercent -= (monthsExpired*.0002)

    lastPrice = lastPricesDictionary[spotifyURI]


    resultsDYT = resultsYT.split("rating average='")[1]

    rating = int(resultsDYT.split("'", 1)[0])/5
    numraters = resultsDYT.split("numRaters='")[1].split("'",1)[0]
    viewcount = resultsDYT.split("viewCount='")[1].split("'",1)[0]

    print viewcount

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


    #################################################
    # Populate database
    #################################################
    change = 0
    body = { 'user_email':email, 'user_token':token, 'song[name]':rawTitle, 'song[artist_name]':rawArtist, 'song[price]':price, 'song[ipo_value]':price, 'song[change]':change }

    apiCHANGEURL = 'http://api.thesongmarket.com/v1/songs/'+str(songID)+'/song_changes'

    if (not(foundFlag)):
        createIPO(spotifyURI)
    else:
        continue
