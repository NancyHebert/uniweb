"""
This module provides configuration to all of the other modules in this application.

It retrieves configuration information from etcd.
"""
# import etcd
import json
# from etcd.client import Client
import os
from collections import defaultdict


class Configuration:


    def getConfig(self):
        return {
                "UNIWeb": {
                    "base_URL": "https://uniweb.uottawa.ca",
                    "token_route": "/api/token.php",
                    "username": "",
                    "password": "",
                    "resource_route": "/api/resource.php",
                    "unit": "Faculty of Medicine"
                },
                "sections": [
                    {"page": "profile", "name": "membership_information"},
                    {"page": "profile", "name": "selected_publications"},
                    {"page": "profile", "name": "research_description"},
                    {"page": "profile", "name": "research_interests"},
                    {"page": "profile", "name": "biography"},
                    {"page": "cv", "name": "research_funding_history"},
                    {"page": "cv", "name": "activities"},
                    {"page": "cv", "name": "user_profile"}                    
                ],
                "cache": {
                    # "host": "redis",
                    "host": "10.0.2.15", #change for testing on local environment don't forget to change back
                    "port": 6379
                }
        }

def getUNIWebConfigs():
    # print(Configuration().getConfig()['UNIWeb'])
    return Configuration().getConfig()['UNIWeb']

def getSections():
    # print(Configuration().getConfig()['sections'])
    return Configuration().getConfig()['sections']

def get_cache_options():
    return Configuration().getConfig()['cache']

class Error(Exception):
    pass

class BadEnvironment(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class ErrorMessage(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
