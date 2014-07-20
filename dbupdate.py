#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# July 19th, 2014
#################################################

import urllib, urllib2
import requests
import json
import HTMLParser
import TSMConstants
import TSMSpotify

# Helper Functions:

def cleanString(dirtyStr):
    return str(HTMLParser.HTMLParser().unescape(dirtyStr))

def createSearchableString(oldStr):
    return oldStr.translate(None, '@#%^&*()<>?:;{}[]-_+=\|')


# Main Script:

songsList = getSongsListFromSpotifyData()
for song in songsList:

    rawTitle = getTitleFromSpotifyData()
    cleanTitle = cleanString(rawTitle)
    searchableTitle = createSearchableString(cleanTitle)

    rawArtist = getArtistFromSpotifyData()
    cleanArtist = cleanString(rawArtist)
    searchableArtist = createSearchableString(cleanTitle)

    searchableQuery = searchableTitle + searchableArtist

    spotifyURL = getSpotifySearchURL()
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

    rating = resultsDYT.split("'", 1)[0]
    numraters = resultsDYT.split("numRaters='")[1].split("'",1)[0]
    viewcount = resultsDYT.split("viewCount='")[1].split("'",1)[0]

    print rating
    print numraters
    print viewcount

    req2 = urllib2.Request(searchURL)
    response2 = urllib2.urlopen(req2)
    spotify_page = response2.read(1400)

    try:
        track = spotify_page.split('<album', 2)[1]
        album = track.split('<name>',1)[1].split('</name>',1)[0].split(" [")[0].replace("'", "''")
        print album
    except IndexError:
        pass


    price = float(track.split('<popularity>',1)[1].split('</popularity>',1)[0])*100
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
        if result['name']==title and result['artist_name']==artist:
            print 'FOUND IT!'
            oldPrice = result['price']
            foundFlag = True;
            songID = result['id']
            break


    #################################################
    # Populate database
    #################################################
    change = 0
    body = { 'user_email':email, 'user_token':token, 'song[name]':title, 'song[artist_name':artist, 'song[price]':price, 'song[change]':change }

    if (foundFlag):
        change = price - oldPrice
        apiPUTURL += '/' + str(songID)
        p = requests.put(apiPUTURL, data=body)
        print "PUT!"

    else:
        p = requests.post(apiPOSTURL, data=body)
        print p.status_code
        print p.text
    break
