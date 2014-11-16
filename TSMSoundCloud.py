import soundcloud
import urllib2

# create a client object with your app credentials
client = soundcloud.Client(client_id='f511dbdda52d380951938b5cede62ce8')

# find all sounds of buskers licensed under 'creative commons share alike'
tracks = client.get('/tracks', q='good charlotte girls and boys', limit=1)

for track in tracks:
    print track.title
    print track.playback_count
    print track.favoritings_count
    print track.user


url = "http://ws.audioscrobbler.com/2.0/?method=track.search&track=Believe&api_key=4d1246dbbf181d5139405d9e3f272281&format=json&limit=1"

spotifyRequest = urllib2.Request(url)
spotifyResponse = urllib2.urlopen(spotifyRequest)
spotifyData = spotifyResponse.read()

