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
import sets
import sys
import time
from urlparse import urlparse
from urlparse import urlunparse

from http.http_connection import HttpConnection
from http.http_request import HttpRequest
from http.http_response import HttpResponse
from http.http_entity_builder import HttpEntityBuilder

HTTP_SUCCESS = sets.Set([200,201,202])

class RancherClient(object):
    def __init__(self, host, port, username, password):
        print "Executing method __init__() in class RancherClient in file RancherClient.py\n"
        self.baseUrl = urlunparse(('http', '%s:%s' % (host,port), '', '', '', ''))
        self.http_connection = HttpConnection(self.baseUrl, username, password)
        self.request = HttpRequest(self.http_connection, username, password)
  # End __init__

    @staticmethod
    def createClient(host, port, username, password):
        print "Executing method createClient() in class RancherClient class in file RancherClient.py\n"
        return RancherClient(host, port, username, password)

    def createStack(self, projectId, stackName, dockerCompose, rancherCompose):
        print "Executing method createStack() in class RancherClient in file RancherClient.py with parameters projectId=%s, stackName=%s" % (projectId, stackName)
        createStackUrlString = 'v2-beta/projects/%s/stacks?name=%s&dockerCompose=%s&rancherCompose=%s' % (projectId, stackName, dockerCompose, rancherCompose)
        r = self.request.post(createStackUrlString, None, contentType='application/json')
        if r.getStatus() in HTTP_SUCCESS:
            return json.loads(r.getResponse())
        else:
            self.throw_error(r)

    def upgradeRancherServices(self, projectName, stackName, serviceName):
        print "Executing method upgradeRancherServices() in class RancherClient class in file RancherClient.py\n"
        projectUrlString = 'v2-beta/projects?name=%s' % projectName
        r = self.request.get(projectUrlString, contentType = 'application/json')
        if r.getStatus() in HTTP_SUCCESS:
            response = json.loads(r.response)
        else:
            self.throw_error(r)
        stacksLink = response['data'][0]['links']['stacks']
        print "Stacks link is %s\n" % stacksLink

        stacksUrlString = "%s?name=%s" % (urlparse(stacksLink).path[1:], stackName)
        r = self.request.get(stacksUrlString, contentType = 'application/json')
        if r.getStatus() in HTTP_SUCCESS:
            response = json.loads(r.response)
        else:
            self.throw_error(r)
        servicesLink = response['data'][0]['links']['services']
        print "Services link is %s\n" % servicesLink

 # Note service filtering does not work; this call returns a collection of all services in the stack.
        servicesUrlString = "%s?name=%s" % (urlparse(servicesLink).path[1:], serviceName)
        r = self.request.get(servicesUrlString, contentType = 'application/json')
        if r.getStatus() in HTTP_SUCCESS:
            response = json.loads(r.response)
        else:
            self.throw_error(r)
        for service in response['data']:
            if service['name'] != serviceName:
                continue
            if service['state'] != 'active':
                print "%s cannot be upgraded because its current state is %s" % (service['name'], service['state'])
                sys.exit(1)
            print "Upgrading %s, state was %s\n" % (service['name'], service['state'])
            selfLink = service['links']['self']
            selfUrlString = urlparse(selfLink).path[1:]
            upgradeLink = service['actions']['upgrade']
            print "Upgrading with upgradeLink %s\n" % upgradeLink

            if service['upgrade']:       
                upgradeConfig = service['upgrade']['inServiceStrategy']
            else:
                upgradeConfig = None

            upgradeRequestBody = {"inServiceStrategy":upgradeConfig,"toServiceStrategy": None}
       
            upgradeUrlString = urlunparse(('', '', urlparse(upgradeLink).path, '', urlparse(upgradeLink).query, ''))[1:]
            print "upgradeUrlString = %s\n" % upgradeUrlString
            r =self.request.post(upgradeUrlString, HttpEntityBuilder.create_string_entity(json.dumps(upgradeRequestBody)), contentType='application/json')
            if r.getStatus() not in HTTP_SUCCESS:
                self.throw_error(r)
        
            if self.getStateAfterTransitioning(selfUrlString) == 'upgraded':
                print "Service has been upgraded"
            else:
                print "Service has not been upgraded; do rollback\n"

    # End upgradeRancherServices

    def getStateAfterTransitioning(self, serviceUrlString):
        print "Executing method getStateAfterTransitioning() in class RancherClient class in file RancherClient.py\n"
        r = self.request.get(serviceUrlString, contentType = 'application/json')
        response = json.loads(r.response)
        serviceTransitioning = response['transitioning']
        pollCount = 0
        while serviceTransitioning != 'no':
            time.sleep(10)
            pollCount = pollCount + 1
            print "Transitioning, waiting... %d\n" % pollCount
            r = self.request.get(serviceUrlString, contentType = 'application/json')
            if r.getStatus() in HTTP_SUCCESS:
                response = json.loads(r.response)
            else:
                self.throw_error(r)
            serviceTransitioning = response['transitioning']
        r = self.request.get(serviceUrlString, contentType = 'application/json')
        if r.getStatus() in HTTP_SUCCESS:
            response = json.loads(r.response)
        else:
            self.throw_error(r)
        return response['state']

    def throw_error(self, response):
        print "Executing method throw_error() in class RancherClient in file RancherClient.py\n"
        print "Error from Rancher, HTTP Return: %s\n" % (response.getStatus())
        sys.exit(1)
        
# End RancherClient
