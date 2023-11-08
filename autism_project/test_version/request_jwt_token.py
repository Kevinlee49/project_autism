# To get JWT Token - returnzero api

# import requests

# CLIENT_ID = 'jqOyfqEsB2nxKHHcOq6G'
# CLIENT_SECRET = 'X3rq_TCTl5qojuqONOrOnqrz2l9bO3cur5D3xu6c'

# #Client ID, Client Secret
# #jqOyfqEsB2nxKHHcOq6G, X3rq_TCTl5qojuqONOrOnqrz2l9bO3cur5D3xu6c

# resp = requests.post(
#     'https://openapi.vito.ai/v1/authenticate',
#     data={'client_id': '{CLIENT_ID}',
#           'client_secret': '{CLIENT_SECRET}'}
# )
# resp.raise_for_status()
# print(resp.json())

import requests

# Replace with your actual client_id and client_secret
client_id = 'jqOyfqEsB2nxKHHcOq6G'
client_secret = 'X3rq_TCTl5qojuqONOrOnqrz2l9bO3cur5D3xu6c'

# Set up the headers
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Set up the data payload
data = {
    'client_id': client_id,
    'client_secret': client_secret
}

# Send the request
response = requests.post(
    'https://openapi.vito.ai/v1/authenticate',
    headers=headers,
    data=data
)

# Raise an exception if the request was unsuccessful
response.raise_for_status()

# Print the response
print(response.json())

# {'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTk0MDU1NDMsImlhdCI6MTY5OTM4Mzk0MywianRpIjoiMHJZUjY3TTNLUlZ0QWczUEVrVmsiLCJwbGFuIjoiYmFzaWMiLCJzY29wZSI6InNwZWVjaCIsInN1YiI6ImpxT3lmcUVzQjJueEtISGNPcTZHIiwidWMiOmZhbHNlfQ.m3H3fJv-ZXgJx_ofZ_P1n53bar1CQ7SWR_770r1RMCA', 'expire_at': 1699405543}