import urllib, urllib2, ast
import json

# url_2 = 'http://api.thesongmarket.com/v1/songs'
# values = {'user_email':'mattyayoh@gmail.com', 'user_token':'PQBTwrEmyRJrR8GMs6ij', 'song[name]':'Dark Horse', 'song[price]':666, 'song[change]':3, 'song[artist_name]':'Katy Perry', 'song[album_name]':'I Dont Know', 'song[market_name]':'Pop'}
# data = urllib.urlencode(values)
# req = urllib2.Request(url_2, data)
# rsp = urllib2.urlopen(req)
# content = rsp.read()

# # print result
# print content
email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'


url = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token


data = json.load(urllib2.urlopen(url))['results']
count = 0
for result in data:
    print result
    print
    count+=1
    # if result['name']=='Dark Horse' and result['artist_name']=='Katy Perry':
    #     print 'FOUND IT!'
    #     break


print count
