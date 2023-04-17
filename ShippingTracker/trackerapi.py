import requests
from django.conf import settings
import json

class TrackingShippingAPI:
    def __init__(self):
        self.API_Key = settings.TRACKING_CLIENT_ID
        self.Secret = settings.TRACKING_CLIENT_SECRET
        self.url = 'https://api.reachship.com/sandbox/v1/oauth/token'
        

    def apiauth(self):
 
        param = {
            "grant_type":"client_credentials" ,
            "client_id": self.API_Key,
             "client_secret": self.Secret, 
        }

        

        headers = {
            'Content-Type':'application/x-www-form-urlencoded'
        }
        # requests.get(url, headers = headers, params=params, json=json)
        response = requests.get( self.url, headers=headers, params=param)

        return response.json()
    def access_token(self):
        accesstoken = self.apiauth["access_token"]
        return accesstoken

    def trackshipping(self, carrier_name,tracking_number):
        
        url = "https://api.reachship.com/sandbox/v1/track-shipment"
        
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        body = {
            "carrier_name":carrier_name,
            "tracking_number":tracking_number
        }
        response = requests.post(url,headers=headers,data=json.dumps(body))
        return response.json()
        


