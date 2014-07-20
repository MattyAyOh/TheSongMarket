spotifyAPIURL = 'http://ws.spotify.com/search/1/track?q=genre:pop'

def getSongsListFromSpotifyData():
    currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']
    spotifyRequest = urllib2.Request(spotifyAPIURL)
    spotifyResponse = urllib2.urlopen(spotifyRequest)
    spotifyData = spotifyResponse.read()
    return spotifyData.split('<track ')[1:]

def getTitleFromSpotifyData(songData):
    return songData.split('<name>')[1].split('</name>')[0].split(" - ")[0].split(" (From")[0].split(" [")[0].split(" (")[0].replace("'", "")

def getArtistFromSpotifyData(songData):
    return songData.split('<name>')[2].split('</name>')[0].split(" Featuring")[0]

def getSpotifySearchURL(query):
    return "http://ws.spotify.com/search/1/track?q="+query
