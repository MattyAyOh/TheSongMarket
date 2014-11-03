import sqlite3
import json
import urllib2
from IPO import *

db = sqlite3.connect('records.sqlite')
c = db.cursor()
trackID = 2307
c.execute('SELECT youtubeuri, viewcount FROM ytviewcount WHERE trackid=(?)',(trackID,))
row = c.fetchone()
print row[0]
print type(row[0])
lastVC = row[1]
currentPrice = 272

youtubeSURL = "https://www.googleapis.com/youtube/v3/videos?id=" + row[0] + "&key=AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q&part=snippet,statistics"

print youtubeSURL

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

currentDate = datetime.datetime.now()
differenceInDate = (currentDate - publishedDate).days
print differenceInDate
expectedPercent = .01
if( differenceInDate > 90 ):
    daysExpired = differenceInDate - 90
    monthsExpired = int(daysExpired/30)
    print monthsExpired
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

# newPrice = currentPrice + change

#################################################
# Populate database
#################################################
# body = { 'user_email':email, 'user_token':token, 'song[name]':rawTitle, 'song[artist_name]':rawArtist, 'song[price]':price, 'song[ipo_value]':price, 'song[change]':change }
# apiCHANGEURL = 'http://api.thesongmarket.com/v1/songs/'+str(songID)+'/song_changes'
body = {'user_email': email, 'user_token': token, 'song_change[song_id]':trackID, 'song_change[changed_value]':intChange}

print body