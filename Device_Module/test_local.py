# test device_server.py
# must first run device_server.py and then run test.py

import requests

BASE = 'http://127.0.0.1:5000/'

print('read all:')
response = requests.get(BASE + 'patients/')
print(response.json())

readings = {
    'temperature': 98.0,
    'pulse': 80,
    'oxi': 98,
    'weight': 155.5,
    'gluco': 100
}

print('add patient 1 readings:')
response = requests.put(BASE + 'patients/1', readings)
print(response)

print('read patient 1 readings:')
response = requests.get(BASE + 'patients/1')
print(response.json())

readings = {
    'temperature': 99.0
}

print('update patient 1 readings:')
response = requests.put(BASE + 'patients/1', readings)
print(response)

readings = {
    'temperature': 100.0,
    'pulse': 80,
    'oxi': 98,
    'weight': 155.5,
    'gluco': 100
}

print('add patient 2 readings:')
response = requests.put(BASE + 'patients/2', readings)
print(response)

print('read all:')
response = requests.get(BASE + 'patients/')
print(response.json())

print('delete patient 1 readings:')
response = requests.delete(BASE + 'patients/1')
print(response)

print('read patient 1 readings:')
response = requests.get(BASE + 'patients/1')
print(response.json())

print('delete patient 1 again:')
response = requests.delete(BASE + 'patients/1')
print(response)

print('read all:')
response = requests.get(BASE + 'patients/')
print(response.json())

print('delete all:')
response = requests.delete(BASE + 'patients/')
print(response)

print('read all:')
response = requests.get(BASE + 'patients/')
print(response.json())