import json
import requests
import falcon
from data.resources.utils import token
from config import settings
from data.resources.utils import uniweb_options


class Resource:
    section = "cv/activities/teaching_activities/courses_taught" #  contributions/interviews_and_media_relations/broadcast_interviews
    def on_get(self, req, resp, professor_id):
        """Handles POST requests"""
        UNIWebtoken = token.getToken()
        UNIWebConfigs = settings.getUNIWebConfigs()
        requestDict = {
            "action":"read",
            "resources": [self.section], 
            "id": professor_id
        }
        requestStr = json.dumps(requestDict)
        print('requestStr', requestStr)
        try:
            resourceResult = requests.post(UNIWebConfigs['base_URL'] + UNIWebConfigs['resource_route'], verify=False, # TODO remove verify=False on Production
                                       headers={"Content-Type": "application/x-www-form-urlencoded"},
                                       data="access_token=" + UNIWebtoken + "&request=" + requestStr)
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_725,
                                   'UniWeb Connection Error',
                                   'Exception: %s' % e)

        print('resourceResult.content in course_taught: ', resourceResult.content)
        resultJson = json.loads(resourceResult.content.decode('utf-8'))
        # cleanProfObj(resultJson)
        resp.body = json.dumps(resultJson)

        # print(resourceResult.content)
        #TODO: raise error when response contains error. UniWeb always returns 200 !



    def on_post(self, req, resp, professor_id):
        """Handles POST requests"""
        print('courses_taught ', professor_id)        
        UNIWebtoken = token.getToken()
        UNIWebConfigs = settings.getUNIWebConfigs()

        # get data from body
        try:
            body = req.stream.read()
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_748,
                                   'Read Error',
                                   'Could not read the request body.')
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid Json document is required.')
        try:
            data_json = json.loads(body.decode('utf-8'))
            print('data_json: ', data_json)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed Json',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

        # TODO: get the options Id of the following: 
        # organization, academic_session, course_level, guest_lecture
        # academic_sessions = uniweb_options.getOptions(self.section + '/academic_session')
        # print('academic_sessions: ', academic_sessions)

        # TODO: replace values by id for organization, academic_session, course_level, and guest_lecture 

        sectionData = [{
            ##"lecture_hours_per_week": data_json['hours'],
            "course_title": data_json['course_title'],
            ##"end_date": data_json['end_date'], #"2025-1-1",
            # "number_of_students": "22",
            # "academic_session": "1",
            #"section": "section",
            ##"number_of_credits": data_json['credit'], #,
            # "guest_lecture": "1",
            # "co-instructors": [
            #     {
            #         "family_name": "co-inst last",
            #         "first_name": "co-inst first"
            #     }
            # ],
            # "course_level": "1",
            # "tutorial_hours_per_week": "1",
            "role": data_json['role'], #,
            # "lab_hours_per_week": "1",
            # "department": "dept",
            # "organization": "33", # UO
            "course_code": data_json['course_code'], #"code",
            ##"start_date": data_json['start_date'] #, #"2026-1-1",
            # "course_topic": "topic"
        }]
        requestDict = {
            "action":"add",
            "resources": { self.section: sectionData }, # data_json
            "id": professor_id
        }
        requestStr = json.dumps(requestDict)
        print('requestStr', requestStr)
        try:
            resourceResult = requests.post(UNIWebConfigs['base_URL'] + UNIWebConfigs['resource_route'], verify=False, # TODO remove verify=False on Production
                                       headers={"Content-Type": "application/x-www-form-urlencoded"},
                                       data="access_token=" + UNIWebtoken + "&request=" + requestStr)
        except Exception as e:
            print('error: '. e)
            raise falcon.HTTPError(falcon.HTTP_725,
                                   'UniWeb Connection Error',
                                   'Exception: %s' % e)

        # print('courses_taught resourceResult: ', resourceResult)
        print('courses_taught resourceResult content: ', resourceResult.content.decode('utf-8'))

        resp.status = falcon.HTTP_201

        # resultJson = json.loads(resourceResult.content.decode('utf-8'))
        # cleanProfObj(resultJson)
        # resp.body = json.dumps(resultJson)

        # print(resourceResult.content)
        #TODO: raise error when response contains error. UniWeb always returns 200 !