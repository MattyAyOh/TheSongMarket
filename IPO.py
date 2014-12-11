#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# Sept 28th, 2014
#################################################

from TSMSpotify import *
from TSMCommon import *
import requests
import sys
import sqlite3

email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'
rawTitle = ""
rawArtist = ""


def generateIPO(songURI, trackID):
    songData = requestResponse(getSpotifyLookupURL(songURI))

    global rawTitle
    rawTitle = getTitleFromSpotifyData(songData)
    cleanTitle = cleanstring(rawTitle)
    searchableTitle = createsearchablestring(cleanTitle)

    global rawArtist
    rawArtist = getArtistFromSpotifyData(songData)
    cleanArtist = cleanstring(rawArtist)
    searchableArtist = createsearchablestring(cleanArtist)

    searchableQuery = searchableTitle.replace(" ", "%20") + "%20" + searchableArtist.replace(" ", "%20")

    youtubeSURL = "http://gdata.youtube.com/feeds/api/videos?q=" + searchableQuery + "&orderby=viewCount&max-results=1"
    youtubeData = requestResponse(youtubeSURL)

    published = youtubeData.split("<published>")[1].split("</published>")[0]
    publishedDate = getDateUtilFromString(published)

    currentDate = datetime.datetime.now()
    differenceInDate = (currentDate - publishedDate).days

    scale = 1

    if(differenceInDate < 14):
        scale += (5*((14-differenceInDate)/14))

    youtubeRating = float(youtubeData.split("rating average='")[1].split("'", 1)[0])/5

    numraters = int(youtubeData.split("numRaters='")[1].split("'",1)[0])
    viewcount = int(youtubeData.split("viewCount='")[1].split("'",1)[0])

    totalYTPoints = numraters + viewcount

    totalYTPoints *= scale

    price = 0
    if totalYTPoints <= 1000: #1K Bracket
        price = 10

    elif totalYTPoints > 1000 and totalYTPoints <= 10000: #10K Bracket
        price = (((totalYTPoints-1000.0)/9000.0)*40)+10
    elif totalYTPoints > 10000 and totalYTPoints <= 100000: #100K Bracket
        price = (((totalYTPoints-10000.0)/90000.0)*50)+50
    elif totalYTPoints > 100000 and totalYTPoints <= 1000000: #1 Milo Bracket
        price = (((totalYTPoints-100000.0)/900000.0)*400)+100
    elif totalYTPoints > 1000000 and totalYTPoints <= 10000000: #10 Milo Bracket
        price = (((totalYTPoints-1000000.0)/9000000.0)*500)+500
    elif totalYTPoints > 10000000 and totalYTPoints <= 100000000: #100 Milo Bracket
        price = (((totalYTPoints-10000000.0)/90000000.0)*4000)+1000
    elif totalYTPoints > 100000000: #1 Bilo Bracket
        price = (((totalYTPoints-100000000.0)/900000000.0)*5000)+5000

    popularity = getPopularityFromSpotifyData(songData)

    overallPerformance = (popularity + youtubeRating)/2
    finalIPOPrice = price*overallPerformance

    apiGETSONGURL = "http://api.thesongmarket.com/v1/songs/"+str(trackID)+"?user_email="+email+"&user_token="+token
    p = requests.get(apiGETSONGURL)
    mydict = p.json()
    artistID = mydict["results"]["artist_id"]

    db = sqlite3.connect('/home/deploy/thesongmarket_python_scripts/records.sqlite')
    c = db.cursor()

    c.execute('SELECT average FROM artistaverages WHERE artistid=(?)', (artistID,))
    row = c.fetchone()
    artistAvgPrice = 0
    if(row != None):
        artistAvgPrice = row[0]
    if finalIPOPrice < artistAvgPrice:
        finalIPOPrice = (artistAvgPrice+finalIPOPrice)/2

    if finalIPOPrice < 10:
        finalIPOPrice = 10

    # c.execute('INSERT OR REPLACE INTO iporecords VALUES (?,?,?,?,?,?,?)', (trackID, viewcount, youtubeRating, numraters, popularity, artistAvgPrice,finalIPOPrice))
    # db.commit()
    # db.close()

    return finalIPOPrice

def publishIPO(songID, ipo):
    # market = "Mainstream"
    body = {'user_email': email, 'user_token': token, 'song[ipo_value]': ipo}
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    # print body
    apiUPDATEURL = 'http://api.thesongmarket.com/v1/songs/' + str(songID)
    p = requests.put(apiUPDATEURL, data=body, headers=headers)
    print p.status_code
    print p.text



def createIPO(songURI, TSMTrackID=-1):
    #TODO: Check if song is 3 days old on youtube
    print songURI
    print TSMTrackID
    if(checkTrackIDExists(TSMTrackID)):
        finalIPOPrice = generateIPO(songURI,TSMTrackID)
        publishIPO(TSMTrackID, finalIPOPrice)

listofArgs = sys.argv[1:]
for arg in listofArgs:
    print arg
    argsSplit = arg.split(",")
    uri = argsSplit[0]
    id = 0
    try:
        id = int(argsSplit[1])
    except ValueError:
        id = -1
    createIPO(uri, id)
