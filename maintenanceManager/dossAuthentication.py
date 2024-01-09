import requests
import json
import os
from dotenv import load_dotenv

def getCredentuals():
    load_dotenv()
    username = os.environ["dossUsername"]
    password = os.environ["dossPassword"]
    secret = os.environ["client_secret"]

    return username, password, secret

def getAccessToken():
    username, password, secret = getCredentuals()
    return getAccessTokenWithCreds(username=username, password=password, secret=secret)

def getAccessTokenWithCreds(username, password, secret): 
    # Set the URL for the POST request
    url = 'https://authentication.d7.dossierondemand.com/connect/token'


    # Define the data to be sent in the request body
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'scope': 'DossierApi',
        'client_id': 'sharpTransportationClient',
        'client_secret': secret
    }

    # Make the POST request with x-www-form-urlencoded data
    response = requests.post(url, data=data, verify=False)

    # Check the response status code
    if response.status_code == 200:
        print("Authentication was successfull.")
        try:
            response_data = json.loads(response.text)
            access_token = response_data.get('access_token')
            return access_token
        except:
            print("unable to parse json")
            return False
    else:
        print(f"Error: {response.status_code}")
        print("Response:", response.text)


if __name__ == "__main__":

    

    print(getAccessToken(getCredentuals()))