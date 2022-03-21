
import requests

BASE = 'http://127.0.0.1:5000/'


msg = {
    'sender_id': 1,
    'recipient_id': 2,
    'content' : 'Hello user 1'
}

query = {
    'sender_id': 1,
    'receiver_id': 2,
}

response = requests.post(BASE + 'messages/', msg)
print(response)
print(response.json())
response = requests.get(BASE + 'messages/', query)
print(response)
print(response.json())




