#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# July 19th, 2014
#################################################

import json
import sqlite3
from IPO import *
from ytvcUpdate import *

apiPOSTURL = 'http://api.thesongmarket.com/v1/songs'
apiGETURL = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token

#################################################
# Main Script
#################################################

currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']

db = sqlite3.connect('records.sqlite')
c = db.cursor()

for song in currentListOfDictOfSongs:
    spotifyURI = song['spotify_uri']
    trackID = int(song['id'])
    c.execute('youtubeuri, viewcount FROM ytviewcount WHERE trackid=(?)', (trackID,))
    row = c.fetchone()
    if(row == None):
        #Couldn't find row from db
        continue
    try:
        currentPrice = int(song['price'])
    except TypeError:
        # print "No IPO Yet!"
        continue
    if currentPrice <= 0:
        print song['name'] + " - " + song['artist_name'] + " - Bankrupt!"
        continue
    try:
        lastVC = int(row[1])
        print "Last VC: %d" % lastVC
        youtubeURI = row[0]
    except KeyError:
        print "Song not found in last VC CSV!"
        continue

    songID = song['id']
    print "SONG ID: %s" % songID
    print "YOUTUBE URI: %s" % youtubeURI

    youtubeSURL = "https://www.googleapis.com/youtube/v3/videos?id=" + youtubeURI + "&key=AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q&part=snippet,statistics"

    while(True):
        try:
            youtubeJSON = json.load(urllib2.urlopen(youtubeSURL))
        except urllib2.HTTPError:
            print "HTTP ERROR!"
            continue
        break

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
        change = -(float(pow((.02-performancePercent),2)/pow(expectedPercent,2)*10))


    intChange = 2*int(round(change))
    print "Change: %d" % intChange
    if(intChange > 10 or intChange < -10):
        intChange /= 10
        print "Reducing Change!"
    print currentPrice

    if((currentPrice + intChange)<= 0):
        intChange = -(currentPrice-1)
        print "GOING BANKRUPT!!!"

    #################################################
    # Populate database
    #################################################
    body = {'user_email': email, 'user_token': token, 'song_change[song_id]':songID, 'song_change[changed_value]':intChange}

    headers = {'content-type': 'application/x-www-form-urlencoded'}

    apiUPDATEURL = 'http://api.thesongmarket.com/v1/songs/'+str(songID)+'/song_changes'
    p = requests.post(apiUPDATEURL, data=body, headers=headers)
    print p.status_code
    print p.text


db.close()