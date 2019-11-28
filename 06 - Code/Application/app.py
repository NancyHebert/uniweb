#!/usr/bin/env python3
"""
    Auth.py: This is the main program. It is a simple service that authenticates a user
    using a username and a password. This service has one route: /auth and only has a need
    to support a post request.

    The service uses multiple strategies contained in the authentication folder.

    This service call can launched is a few different ways, but here is an example of one of the ways:
    gunicorn auth:app --keyfile certs/medtechauth.ca-2016-03-28-145510.pkey --certfile certs/medtechauth.ca-2016-03-28-145510.cer  -b :443 -D

    The above command will launch the program so that is listens on port 443 for SSL/HTTPS requests.

    To learn more about the launch options, read the Gunicorn documentation at: http://docs.gunicorn.org/en/stable/
"""

__author__      = "Jim Cassidy, Sadek Hamdan"
__copyright__   = "Copyright 2016 by The University of Ottawa, faculty of Medicine."
__license__     = "TBD"
__status__      = "Development"
__version__     = "0.01.01"

import json
import falcon
from falcon_cors import CORS
from data.resources import professor, professors, professorsResource, courses_taught
import locale
import socket

cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)
locale.setlocale(locale.LC_ALL, '') # Set locale in app so sorting works properly

api = falcon.API(middleware=[cors.middleware])

api.add_route('/professors', professors.Resource())
api.add_route('/professors/resource/{section}', professorsResource.Resource())
api.add_route('/professors/{professor_id}', professor.Resource())
api.add_route('/professors/{professor_id}/courses_taught', courses_taught.Resource())
# api.add_route('/courses_taught/{professor_id}', courses_taught.Resource())

# Set up "/heartbeat", to check whether server is up
class HeartBeat:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': 'Server Up, Captain',
            'author': 'Scotty',
            'hostname': socket.gethostname()
        }

        resp.body = json.dumps(quote)

api.add_route("/heartbeat", HeartBeat())
