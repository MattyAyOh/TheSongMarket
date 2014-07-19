import urllib, urllib2, ast
import requests
import json

email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'
url = "http://api.thesongmarket.com/v1/songs"

url = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token


data = json.load(urllib2.urlopen(url))['results']

songTitle = 'Longview'
songArtist = 'Green Day'
search = {'name': songTitle, 'artist_name': songArtist}.viewitems()


while(True):
    foundFlag = False
    for result in data:
        if result['name']=='Dark Horse' and result['artist_name']=='Katy Perry':
            print 'FOUND IT!'
            foundFlag = True;
            break
    if(foundFlag):
        break

    body = { 'user_email':email, 'user_token':token, 'song[name]':songTitle, 'song[price]':50, 'song[change]':1 }
    p = requests.post(url, data=body)

    print p.status_code
    print p.text
    print "COMPLETE!"
    break
