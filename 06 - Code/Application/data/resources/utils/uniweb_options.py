import json
import requests
from data.resources.utils import token
from config import settings


def getOptions(section):
    """Handles POST requests"""
    UNIWebtoken = token.getToken()
    UNIWebConfigs = settings.getUNIWebConfigs()
    requestDict = {
        "action":"options",
        "resources": section
    }
    requestStr = json.dumps(requestDict)
    print('requestStr', requestStr)

    resourceResult = requests.post(UNIWebConfigs['base_URL'] + UNIWebConfigs['resource_route'], verify=False, # TODO remove verify=False on Production
                                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                                    data="access_token=" + UNIWebtoken + "&request=" + requestStr)


    print('options for ', section, ' are: ', resourceResult.content)
    return '1'
    # print('courses_taught resourceResult content: ', resourceResult.content)
    # resp.status = falcon.HTTP_200  

    # print(resourceResult.content)
    #TODO: raise error when response contains error. UniWeb always returns 200 !