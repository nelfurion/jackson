import requests

from config import config

endpoints = config['summarization_endpoints']

body = {
    "text": "Dashwood contempt on mr unlocked resolved provided of of",
	"title": "Animal",
	"adjectives": ["biggest"],
	"nouns": ["animal"],
	"adjective_phrases": [],
	"noun_phrases": []
}

for endpoint in endpoints:
    print('Waking up ', endpoint)
    request = requests.post(endpoint, json=body)
    print(request.text)