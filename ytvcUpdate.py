#################################################
# Property of The Song Market
#
# Update csv of Last Prices.  Run this daily
#
# Created by: Matt Ao
# Sept 25th, 2014
#################################################

import json
import urllib2
import csv

email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'

apiGETURL = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token

currentListOfDictOfSongs = []

dictionaryPrices = {}

currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']

for song in currentListOfDictOfSongs:

    spotifyURI = song['spotify_uri']
    print spotifyURI
    if spotifyURI in dictionaryPrices:
        continue
    else:
        dictionaryPrices[spotifyURI] = int(song['price'])

w = csv.writer(open("lastPrices.csv", "w+"))
for key, val in dictionaryPrices.items():
    w.writerow([key, val])