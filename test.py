import requests
email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'

CurrentVC = 210794
LastVC = 205922
differenceVC = CurrentVC - LastVC
print differenceVC
print CurrentVC
performancePercent = float(float(differenceVC)/float(CurrentVC))

print performancePercent

expectedPercent= .01
change = float(pow(performancePercent,2)/pow(expectedPercent,2)*10)
print change

body = {'user_email': email, 'user_token': token, 'song[price]': 110}
headers = {'content-type': 'application/x-www-form-urlencoded'}

apiUPDATEURL = 'http://api.thesongmarket.com/v1/songs/2601'
p = requests.put(apiUPDATEURL, data=body, headers=headers)