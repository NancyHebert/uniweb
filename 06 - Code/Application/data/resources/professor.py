import json
import requests
import falcon
from data.resources.utils import token
# from data.models.sections import sections
from config import settings
from data.resources.utils.data_cleaning import cleanProfObj
from data.resources.utils.lastModDate import getLastModDate
# from data.resources.utils.data_cleaning import cleanProfessorsList

# from data.models.professor_sections import professor_sections
from data.resources.utils.sections import concatPagesSections


class Resource:
    # won't use rematch decorator for now, as professor_id can be an integer
    # (UNIWEB id) or string (AD username)
    def on_get(self, req, resp, professor_id):
        """Handles POST requests"""
        try:
            professorSections = settings.getSections()
            concatProfessorSections = concatPagesSections(professorSections)
            print(concatProfessorSections)
            lastModifiedDate = getLastModDate()
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_725,
                                   'Database Error',
                                   'DB exception: %s' % e)

        UNIWebtoken = token.getToken()
        UNIWebConfigs = settings.getUNIWebConfigs()
        profsRequestDict = {
            # "language": "fr",
            "action": "read",
            "resources": concatProfessorSections
        }
        # UNIWeb API reacts differently when the prof id is the UNIWeb id or the username
        # supply the proper filter parameters in each case
        if professor_id.isdigit():
            profsRequestDict["id"] = professor_id
        else:
            profsRequestDict["filter"] = {
                "title": "Professor",
                "loginName": professor_id
            }

        profsRequestStr = json.dumps(profsRequestDict)
        print('profsRequestStr', profsRequestStr)
        try:
            resourceResult = requests.post(UNIWebConfigs['base_URL'] + UNIWebConfigs['resource_route'], # verify=False,  # TODO remove verify=False on Production
                                           headers={
                                               "Content-Type": "application/x-www-form-urlencoded"},
                                           data="access_token=" + UNIWebtoken + "&request=" + profsRequestStr)
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_725,
                                   'UniWeb Connection Error',
                                   'Exception: %s' % e)

        resultJson = json.loads(resourceResult.content.decode('utf-8'))
        # UNIWeb API reacts differently when the prof id is the UNIWeb id or the username
        # when using UNIWeb id, the API doesn't return the id, so here we add it to the result 
        if professor_id.isdigit():
            resultJson = { professor_id: resultJson }
        # print('resultJson: ', resultJson)
        if not resultJson or 'error' in resultJson:
            resp.body = json.dumps(resultJson)            
        else:
            cleanResult = cleanProfObj(resultJson)
            profId = cleanResult['id']
            if profId in lastModifiedDate:
                lastUpdateDate = lastModifiedDate[profId]
                cleanResult['lastUpdateDate'] = lastUpdateDate

            resp.body = json.dumps(cleanResult)

        # print(resourceResult.content)
        # TODO: raise error when response contains error. UniWeb always returns
        # 200 !
