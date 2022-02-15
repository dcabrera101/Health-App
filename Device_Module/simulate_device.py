
import sys
from device_api import ingest_data

try:
    filepath = sys.argv[1]
except:
    print('pass filepath as argument')
    exit()

print('opening:', filepath)

with open(filepath) as f:
    status, msg = ingest_data(f)

if status:
    print("Valid")
else:
    print(msg)





