"""
This helper return a UNIWeb token to be used in quering UNIWeb resources
It checks if a valid (not expired) UNIWeb token exists in the database, otherwise
"""
from config import settings
import requests
import json

def getToken():
    # TODO: check if a valid token exists in the database
    # if(token exists & valid)
    #    return it
    # else get a new token from UNIWeb
    try:
        UNIWebConfigs = settings.getUNIWebConfigs()
        tokenResult = requests.post(UNIWebConfigs['base_URL'] + UNIWebConfigs['token_route'], verify=False, #TODO remove verify=False on Production
                                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                                    data="grant_type=password&username=" + UNIWebConfigs['username'] + "&password=" + UNIWebConfigs['password'])

        response = tokenResult.json()
        if response is None:
            return None # TODO raise an error
        # print('token: ', response)
        token = response["access_token"]
        print('token: ', token)
        return token

    except Exception:
        raise

