import requests

BASE = 'http://127.0.0.1:5000/'

readings = {
    'temperature': 98.0,
    # "bp" : [120, 80],
    'pulse': 80,
    'oxi': 98,
    'weight': 155.5,
    'gluco': 100
}

response = requests.get(BASE + 'patients/1')
print(response.json())

response = requests.put(BASE + 'patients/1', readings)
print(response.json())