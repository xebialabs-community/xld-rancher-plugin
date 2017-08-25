#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
        print "Stacks link is %s\n" % stacksLink

        stacksUrlString = "%s?name=%s" % (urlparse.urlparse(stacksLink).path[1:], stackName)
        r = self.request.get(stacksUrlString, contentType = 'application/json')
        response = json.loads(r.response)
        servicesLink = response['data'][0]['links']['services']
        print "Services link is %s\n" % servicesLink

        servicesUrlString = "%s?name=%s" % (urlparse.urlparse(servicesLink).path[1:], serviceName)
        r = self.request.get(servicesUrlString, contentType = 'application/json')
        response = json.loads(r.response)
        for service in response['data']:
            print "%s:  %s\n" % (service['name'], service['state'])
            selfLink = service['links']['self']
            selfUrlString = urlparse.urlparse(selfLink).path[1:]
            upgradeLink = service['actions']['upgrade']
            print "Upgrading with upgradeLink %s\n" % upgradeLink
            # print "service['upgrade'] = %s" % service['upgrade']
            # print "service['upgrade']['inServiceStrategy'] = %s" % service['upgrade']['inServiceStrategy']

            if service['upgrade']:       
                upgradeConfig = service['upgrade']['inServiceStrategy']
            else:
                upgradeConfig = None

            upgradeRequestBody = {"inServiceStrategy":upgradeConfig,"toServiceStrategy": None}
       
            upgradeUrlString = "%s?%s" % (urlparse.urlparse(upgradeLink).path[1:], urlparse.urlparse(upgradeLink).query)
            print upgradeUrlString
            r =self.request.post(upgradeUrlString, HttpEntityBuilder.create_string_entity(json.dumps(upgradeRequestBody)), contentType = 'application/json')
        
            if self.getStateAfterTransitioning(selfUrlString) == 'active':
                print "Service is active"
            else:
                print "Service is not active; do rollback\n"

    # End upgradeRancherServices

    def getStateAfterTransitioning(self, serviceUrlString):
        r = self.request.get(serviceUrlString, contentType = 'application/json')
        response = json.loads(r.response)
        serviceTransitioning = response['transitioning']
        pollCount = 0
        while serviceTransitioning != 'no':
            time.sleep(10)
            pollCount = pollCount + 1
            print "Transitioning, waiting... %d\n" % pollCount
            r = self.request.get(serviceUrlString, contentType = 'application/json')
            response = json.loads(r.response)
            serviceTransitioning = response['transitioning']
        r = self.request.get(serviceUrlString, contentType = 'application/json')
        response = json.loads(r.response)
        return response['state']
        
# End RancherClient
