
import requests

BASE = 'http://127.0.0.1:5000/'


msg1 = {
    'sender_id': 1,
    'recipient_id': 2,
    'content' : 'Hello user 2.'
}

msg2 = {
    'sender_id': 2,
    'recipient_id': 1,
    'content' : 'Hello user 1.'
}

query_recipient = {
    'recipient_id': 1
}

query_sender = {
    'sender_id': 1
}

query_convo = {
    'user A': 1,
    'user B': 2
}

print('\ndelete all msgs:')
response = requests.delete(BASE + 'messages/')
print(response)

print('\npost message:')
response = requests.post(BASE + 'messages/', msg1)
print(response)

print('\npost message:')
response = requests.post(BASE + 'messages/', msg2)
print(response)

msg1['content'] = 'Goodbye.'
print('\npost message:')
response = requests.post(BASE + 'messages/', msg1)
print(response)

msg2['content'] = 'Goodbye.'
print('\npost message:')
response = requests.post(BASE + 'messages/', msg2)
print(response)

print('\nquery by sender_id:')
response = requests.get(BASE + 'messages/', query_sender)
print(response)
print(response.json())

print('\nquery by recipient_id:')
response = requests.get(BASE + 'messages/', query_recipient)
print(response)
print(response.json())

print('\nquery conversation:')
response = requests.get(BASE + 'messages/', query_convo)
print(response)
print(response.json())




