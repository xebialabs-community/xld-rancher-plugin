#
#    THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
#    FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import base64
import json
import time
import urlparse

from http.http_connection import HttpConnection
from http.http_request import HttpRequest
from http.http_response import HttpResponse
from http.http_entity_builder import HttpEntityBuilder

class RancherClient( object ):
    def __init__(self, url, username, password):
      self.url = url
      if url.endswith('/'):
          self.url = url[:-1]
      self.http_connection = HttpConnection(url, username, password)
      self.request = HttpRequest(self.http_connection, username, password)
  # End __init__

    def upgradeRancherServices(self, projectName, stackName, serviceName):
        projectUrlString = 'v2-beta/projects?name=%s' % projectName
        r = self.request.get(projectUrlString, contentType = 'application/json')
        response = json.loads(r.response)
        stacksLink = response['data'][0]['links']['stacks']
        print "Stacks link is %s" % stacksLink

        stackUrlString = "%s?name=%s" % (urlparse.urlparse(stacksLink).path[1:], stackName)
        r = self.request.get(stackUrlString, contentType = 'application/json')
        response = json.loads(r.response)
        servicesLink = response['data'][0]['links']['services']
        print "Services link is %s" % servicesLink

        serviceUrlString = "%s?name=%s" % (urlparse.urlparse(servicesLink).path[1:], serviceName)
        r = self.request.get(serviceUrlString, contentType = 'application/json')
        response = json.loads(r.response)
        for service in response['data']:
            print "%s:  %s" % (service['name'], service['state'])
            selfLink = service['links']['self']
            selfUrlString = urlparse.urlparse(selfLink).path[1:]
            upgradeLink = service['actions']['upgrade']
            print upgradeLink
            print "service['upgrade'] = %s" % service['upgrade']
            print "service['upgrade']['inServiceStrategy'] = %s" % service['upgrade']['inServiceStrategy']
       
            upgradeConfig = service['upgrade']['inServiceStrategy']
            upgradeRequestBody = {"inServiceStrategy":upgradeConfig,"toServiceStrategy": None}
       
            upgradeUrlString = "%s?%s" % (urlparse.urlparse(upgradeLink).path[1:], urlparse.urlparse(upgradeLink).query)
            print upgradeUrlString
            r =self.request.post(upgradeUrlString, HttpEntityBuilder.create_string_entity(json.dumps(upgradeRequestBody)), contentType = 'application/json')
        
            if getStateAfterTransitioning(selfUrlString) == 'active':
                print "Service is active"
            else:
                print "Service is not active; do rollback"


    # End upgradeRancherServices

    def getStateAfterTransitioning(serviceUrlString):
        r = self.request.get(serviceUrlString, contentType = 'application/json')
        response = json.loads(r.response)
        serviceTransitioning = response['data'][0]['transitioning']
        pollCount = 0
        while serviceTransitioning != 'no':
            time.sleep(10)
            pollCount = pollCount + 1
            Print "Transitioning, waiting... %d" % pollCount
            r = self.request.get(serviceUrlString, contentType = 'application/json')
            response = json.loads(r.response)
            serviceTransitioning = response['data'][0]['transitioning']
        r = self.request.get(serviceUrlString, contentType = 'application/json')
        response = json.loads(r.response)
        return response['data'][0]['state']
        
# End RancherClient
