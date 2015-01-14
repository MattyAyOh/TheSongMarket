#################################################
# Property of The Song Market
#
# Spotify Methods
#
# Created by: Matt Ao
# July 19th, 2014
#################################################

import urllib2
spotifyAPIURL = 'http://ws.spotify.com/search/1/track?q=genre:pop'

def getListofSongsFromSpotifyData():
    spotifyRequest = urllib2.Request(spotifyAPIURL)
    spotifyResponse = urllib2.urlopen(spotifyRequest)
    spotifyData = spotifyResponse.read()
    return spotifyData.split('<track ')[1:]

def getTitleFromSpotifyData(songData):
    return songData.split('<name>')[1].split('</name>')[0].split(" - ")[0].split(" (From")[0].split(" [")[0].split(" (")[0].replace("'", "")

def getArtistURIFromSpotifyData(songData):
    artistURI = ""
    try:
        artistURI = songData.split('<artist href="')[1].split('">')[0]
    except IndexError:
        artistURI = getArtistFromSpotifyData(songData)
    return artistURI

def getArtistFromSpotifyData(songData):
    return songData.split('<name>')[2].split('</name>')[0].split(" Featuring")[0]

def getAlbumFromSpotifyData(songData):
    return songData.split('<album href=')[1].split('<name>')[1].split('</name>')[0]

def getSpotifyURIFromSpotifyData(songData):
    return songData.split('<track href="', 1)[1].split('">',1)[0]

def getPopularityFromSpotifyData(songData):
    return float(songData.split('<popularity>')[1].split('</popularity>')[0])

def getSpotifySearchURL(query):
    return "http://ws.spotify.com/search/1/track?q="+query

def getSpotifyLookupURL(songURI):
    return "http://ws.spotify.com/lookup/1/?uri="+songURI