'''
This is a minimal implementation of accessing Schwab API using python.

Prerequisites:
    1. Own a Schwab brokerage account
    2. Be registered on the Schwab API Developer Portal (this is a separate account).
        - You must wait for your account to approved 
        - You must have an App with "Ready For Use" status
        - Fill in the following three pieces of information into the code
            - app_key
            - app_secret
            - auth_callback_url

Note:
    In the production environment, the one time code will be delivered to your specified 
    callback address. Here we will need to manually input to our code.
'''

from pip._vendor import requests
import json
import base64

class SchwabReader():

    def __init__(self):
        # Fill in these information from Schwab Developer Portal
        self.app_key = "<To be filled>"
        self.app_secret = "<To be filled>"
        self.auth_callback_url = "<To be filled>"

        self.encoded_credential = self.encode_credentials()   
        self.access_token = "" # will be set in set_access_token()
        self.api_base_url = "https://api.schwabapi.com/marketdata/v1"
        self.auth_base_url = "https://api.schwabapi.com/v1/oauth/authorize?response_type=code&scope=readonly"
        self.access_token_url = "https://api.schwabapi.com/v1/oauth/token"

    '''
    Encodes app_key and app_secret
    '''
    def encode_credentials(self):
        stringC = self.app_key + ":" + self.app_secret
        encoded = base64.b64encode(stringC.encode("ascii")).decode("ascii")
        return encoded
    
    '''
    Generates URL to obtain one time code. 
    One time code is returned to callback address.
    '''
    def get_one_time_code(self):
        auth_working_url = self.auth_base_url + "&client_id=" + self.app_key + "&redirect_uri=" + self.auth_callback_url
        print(auth_working_url)
        return auth_working_url

    '''
    Gets access token from Schwab API and stores in self.access_token.
    Requires a one time code generated from get_one_time_code()
    '''
    def get_access_token(self, onetimecode):
        postData = {
            "grant_type"    : "authorization_code",
            "code"          : onetimecode,
            "client_id"     : self.app_key,
            "redirect_uri"  : self.auth_callback_url
        }
        headerData = {
            "Authorization" : "Basic " + self.encoded_credential
        }

        x = requests.post(self.access_token_url, data=postData, headers=headerData)
        token = json.loads(x.content)
        self.access_token = token["access_token"]

        #print(json.dumps(token,indent=2))

    '''
    Sample API call
    '''
    def get_StockPrice(self, ticker):
        api_working_url = self.api_base_url + "/quotes?symbols=" + ticker
        x = requests.get(url=api_working_url, headers =  {"Authorization": "Bearer " + self.access_token})
        tickerInfo = json.loads(x.content)
        print(f'TQQQ: {tickerInfo[ticker]["quote"]["lastPrice"]}')

        #print(json.dumps(tickerInfo, indent=2))

'''
Sample Usage
'''
sr = SchwabReader()
sr.get_access_token()
one_time_code =  "<Retrieved from Callback Address>"  
sr.get_access_token(one_time_code)
sr.get_StockPrice("TQQQ")