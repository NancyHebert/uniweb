import json
import grequests
import falcon
import datetime
from data.resources.utils import token
from data.resources.utils.data_cleaning import cleanProfessorsList
from config import settings
from data.resources.utils.sections import concatPagesSections
from data.resources.decorators.cache import cache_response
from pyuca import Collator

class Resource:
    # @cache_response(60*60*24*7)
    def on_get(self, req, resp, section):
        """Handles POST requests"""
        print('section received: ', section)
        section = section.replace('+', '/')
        print('section altered: ', section)        
        UNIWebtoken = token.getToken()
        # print('UNIWebtoken', UNIWebtoken)
        UNIWebConfigs = settings.getUNIWebConfigs()

        allRequests = []
        profsRequestDict = {
            "action": "read",
            "resources": [section],
            "filter": {"title": "Professor", "unit": UNIWebConfigs['unit']}
        }
        profsRequestStr = json.dumps(profsRequestDict)
        print('profsRequestStr', profsRequestStr)
        sectionRequest = grequests.post(UNIWebConfigs['base_URL'] + UNIWebConfigs['resource_route'],
                                        verify=False,  # TODO remove verify=False on Production
                                        headers={
                                            "Content-Type": "application/x-www-form-urlencoded"},
                                        data="access_token=" + UNIWebtoken + "&request=" + profsRequestStr)

        allRequests.append(sectionRequest)

        before = datetime.datetime.now()
        allResponses = grequests.map(allRequests)
        after = datetime.datetime.now()
        print('time total: ', str(after - before))
        # print('responses: ', allResponses)

        profsObject = {}
        for response in allResponses:
            response_json = json.loads(response.content.decode('utf-8'))
            # print('response json: ', response_json)
            if not profsObject:
                profsObject = response_json
            else:
                for k, v in response_json.items():
                    profsObject[k].update(v)

        cleanResult = cleanProfessorsList(profsObject)
        print('profs count: ', len(cleanResult))
        
        # Sort by last name then first name. Use uca to sort french accent characters
        if section == "profile/membership_information":
            c = Collator()
            cleanResult.sort(key=lambda professor: (c.sort_key(professor['membership_information']['last_name'].lower()), c.sort_key(professor['membership_information']['first_name'].lower())))

        resp.body = json.dumps(cleanResult)        
