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

w = csv.writer(open("tempVC.csv", "aw+"))
#################################################
# Main Script
#################################################

if(not(os.path.isfile('lastVC.csv'))):
    createVCPriceDict()

currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']
lastVCDictionary = getLastVCDictionary()
tempVCDictionary = getTempVCDictionary()

for song in currentListOfDictOfSongs:
    spotifyURI = song['spotify_uri']
    if spotifyURI in tempVCDictionary:
        continue

    try:
        currentPrice = int(song['price'])
    except TypeError:
        # print "No IPO Yet!"
        continue

    try:
        lastVC = int(lastVCDictionary[spotifyURI][2].replace(']','').replace(' ',''))
        ytURI = lastVCDictionary[spotifyURI][1]
        youtubeURI = ytURI[-12:-1]
    except KeyError:
        print "Song not found in last VC CSV!"
        continue

    songID = song['id']
    print "SONG ID: %s" % songID
    print "YOUTUBE URI: %s" % youtubeURI

    # rawTitle = song['name']
    # cleanTitle = cleanstring(rawTitle)
    # if cleanTitle == "FAIL":
    #     print "Dirty Title"
    #     print rawTitle
    #     continue
    # searchableTitle = createsearchablestring(cleanTitle)
    #
    # rawArtist = song['artist_name']
    # cleanArtist = cleanstring(rawArtist)
    # if cleanArtist == "FAIL":
    #     print "Dirty Artist"
    #     print rawArtist
    #     continue
    # searchableArtist = createsearchablestring(cleanArtist)
    #
    #
    # searchableQuery = searchableTitle.replace(" ", "%20") + "%20" + searchableArtist.replace(" ", "%20")
    # deprecated
    # youtubeSURL = "http://gdata.youtube.com/feeds/api/videos?q=" + searchableQuery + "&orderby=viewCount&max-results=1"
    youtubeSURL = "https://www.googleapis.com/youtube/v3/videos?id=" + youtubeURI + "&key=AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q&part=snippet,statistics"
    #
    # print youtubeSURL
    # reqYT = urllib2.Request(youtubeSURL)
    # responseYT = urllib2.urlopen(reqYT)
    # results = responseYT.read()

    youtubeJSON = json.load(urllib2.urlopen(youtubeSURL))

    try:
        published = youtubeJSON["items"][0]["snippet"]["publishedAt"]
        publishedDate = getDateUtilFromString(published)
        viewcount = youtubeJSON["items"][0]["statistics"]["viewCount"]
        numraters = youtubeJSON["items"][0]["statistics"]["likeCount"]
    except IndexError:
        print "Failed to Find!"
        continue

    currentDate = datetime.datetime.now()
    differenceInDate = (currentDate - publishedDate).days

    expectedPercent = .01
    if( differenceInDate > 90 ):
        daysExpired = differenceInDate - 90
        monthsExpired = int(daysExpired/30)
        if monthsExpired >= 45:
            expectedPercent = .001
        else:
            expectedPercent -= float(monthsExpired*.0002)


    currentTotalVC = int(numraters) + int(viewcount)
    print "CurrentVC: %d" % (currentTotalVC)
    print "LastVC: %d" % (lastVC)


    differenceVC = currentTotalVC - lastVC
    performancePercent = (float(differenceVC)/float(currentTotalVC))

    #TODO: WHEN 1% away above or below, calculate accordingly
    print "Expected: %f" % (expectedPercent)
    print "Performance: %f" % (performancePercent)

    change = float(pow(performancePercent,2)/pow(expectedPercent,2)*10)

    if performancePercent < expectedPercent:
        change = change*-1



    print change
    print currentPrice

    # newPrice = currentPrice + change

    #################################################
    # Populate database
    #################################################
    # body = { 'user_email':email, 'user_token':token, 'song[name]':rawTitle, 'song[artist_name]':rawArtist, 'song[price]':price, 'song[ipo_value]':price, 'song[change]':change }
    # apiCHANGEURL = 'http://api.thesongmarket.com/v1/songs/'+str(songID)+'/song_changes'
    body = {'user_email': email, 'user_token': token, 'song_change[sond_id]':songID, 'song_change[changed_value]':change}
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    apiUPDATEURL = 'http://api.thesongmarket.com/v1/songs/song_changes'
    p = requests.put(apiUPDATEURL, data=body, headers=headers)

    w.writerow([spotifyURI, (songID, ytURI, currentTotalVC)])


os.remove('lastVC.csv')
os.rename('tempVC.csv', 'lastVC.csv')