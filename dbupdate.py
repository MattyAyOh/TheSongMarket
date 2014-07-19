import unicodedata

import urllib, urllib2
import requests
import json
import HTMLParser

email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'

apiPOSTURL = 'http://api.thesongmarket.com/v1/songs'
apiGETURL = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token
apiPUTURL = 'http://api.thesongmarket.com/v1/songs'

currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']

#################################################
# Grab a list of songs&artists from a website
#################################################

# req = urllib2.Request('http://www.billboard.com/rss/charts/hot-100')
# response = urllib2.urlopen(req)
# the_page = response.read()

req = urllib2.Request('http://ws.spotify.com/search/1/track?q=genre:pop')
response = urllib2.urlopen(req)
the_page = response.read()

#################################################
# Parse web data for the song/artist name
#################################################
# listofSongs =the_page.split('<item>')[1:30]
listofSongs =the_page.split('<track ')[1:]
for song in listofSongs:
    # title = song.split(' ', 3)[3].split('</title>')[0].replace("&#039;", "")
    title = song.split('<name>')[1].split('</name>')[0].split(" - ")[0].split(" (From")[0].split(" [")[0].split(" (")[0].replace("'", "")
    print title
    title = str(HTMLParser.HTMLParser().unescape(title))
    print title
    title = title.translate(None, '@#%^&*()<>?:;{}[]-_+=\|')
    print title

    # artist = song.split('<artist>')[1].split('</artist>')[0].split(" Featuring")[0].split(" &amp;")[0]
    artist = song.split('<name>')[2].split('</name>')[0].split(" Featuring")[0]
    artist = HTMLParser.HTMLParser().unescape(artist)
    artist = artist.translate(None, '!@#$%^&*()<>?:;{}[]-_+=\|')

    #################################################
    # Search spotify for popularity and album
    #################################################

    queryURL = title.replace(" ", "%20") + "%20" + artist.replace(" ", "%20")
    searchURL = "http://ws.spotify.com/search/1/track?q="+ queryURL
    youtubeSURL = "http://gdata.youtube.com/feeds/api/videos?q=" + queryURL + "&orderby=viewCount&max-results=1"
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

