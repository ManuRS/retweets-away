import json

with open('tweet.js', 'r') as f:
	data = json.load(f)

count=0
countb=0
for tweet in data:
	if tweet['full_text'][0:4] != 'RT @':
		print(tweet['full_text']+'\n')
		count+=1
	else:
		countb+=1

print(count)
print(countb)
