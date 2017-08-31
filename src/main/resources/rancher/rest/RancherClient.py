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
    #   print "Executing method __init__() in class RancherClient in file RancherClient.py\n"
        self.baseUrl = urlunparse(('http', '%s:%s' % (host,port), '', '', '', ''))
        self.http_connection = HttpConnection(self.baseUrl, username, password)
        self.request = HttpRequest(self.http_connection, username, password)

    # End __init__

    @staticmethod
    def createClient(host, port, username, password):
    #   print "Executing method createClient() in class RancherClient class in file RancherClient.py\n"
        return RancherClient(host, port, username, password)

    # End createClient

    def validateListLength(self, vList, uniqueMatchOnly):
    #   print "Executing method validateListLength() in class RancherClient class in file RancherClient.py\n"
        if not vList:
            print "No matches found.  Aborting this operation.\n"
            sys.exit(1)
        if uniqueMatchOnly and len(vList) > 1:
            print "Nonunique matches found.  Aborting this operation.\n"
            sys.exit(1)

    # End validateListLength

    def lookupProjectByName(self, projectName):
    #   print "Executing method lookupProjectByName() in class RancherClient in file RancherClient.py with parameters projectName=%s" % (projectName)
        projectUrlLookup = "v2-beta/projects?name=%s" % projectName
        r = self.request.get(projectUrlLookup, contentType = 'application/json')
        if r.getStatus() in HTTP_SUCCESS:
            response = json.loads(r.response)
        else:
            self.throw_error(r)
        projectList = []
        for project in response['data']:
            if project['name'] == projectName:
                projectList.append(project)
        return projectList

    # End lookupProjectByName

    def lookupStackByName(self, project, stackName):
    #   print "Executing method lookupStackByName() in class RancherClient in file RancherClient.py with parameters project=%s, stackName=%s\n" % (project['id'], stackName)
        stacksLink = project['links']['stacks']
        stacksUrlString = "%s?name=%s" % (urlparse(stacksLink).path[1:], stackName)
        r = self.request.get(stacksUrlString, contentType = 'application/json')
        if r.getStatus() in HTTP_SUCCESS:
            response = json.loads(r.response)
        else:
            self.throw_error(r)
        stackList = []
        for stack in response['data']:
            if stack['name'] == stackName:
                stackList.append(stack)
        return stackList

    # End lookupStackByName   

    def createStack(self, project, stackName, dockerCompose, rancherCompose):
    #   print "Executing method createStack() in class RancherClient in file RancherClient.py with parameters projectId=%s, stackName=%s" % (project['id'], stackName)
        createStackUrlString = 'v2-beta/projects/%s/stacks?name=%s&dockerCompose=%s&rancherCompose=%s' % (project['id'], stackName, dockerCompose, rancherCompose)
        r = self.request.post(createStackUrlString, None, contentType='application/json')
        if r.getStatus() in HTTP_SUCCESS:
            return json.loads(r.getResponse())
        else:
            self.throw_error(r)

    # End createStack

    def getStackServices(self, stack):
    #   print "Executing method getStackServices() in class RancherClient in file RancherClient.py with parameters projectId=%s, stackName=%s" % (project['id'], stackName)
        servicesLink = stack['links']['services']
        servicesUrlString = urlparse(servicesLink).path[1:]
        r = self.request.get(servicesUrlString, contentType = 'application/json')
        if r.getStatus() in HTTP_SUCCESS:
            response = json.loads(r.response)
        else:
            self.throw_error(r)
        return response['data']

    # End getStackServices

    def upgradeRancherService(self, service):
    #   print "Executing method upgradeRancherService() in class RancherClient class in file RancherClient.py\n"
        if service['state'] != 'active':
            print "%s cannot be upgraded because its current state is %s" % (service['name'], service['state'])
            sys.exit(1)
        print "Upgrading %s, state was %s\n" % (service['name'], service['state'])
        upgradeLink = service['actions']['upgrade']
        if service['upgrade']:       
            upgradeConfig = service['upgrade']['inServiceStrategy']
        else:
            upgradeConfig = None
        upgradeRequestBody = {"inServiceStrategy":upgradeConfig,"toServiceStrategy": None}
        upgradeUrlString = urlunparse(('', '', urlparse(upgradeLink).path, '', urlparse(upgradeLink).query, ''))[1:]
        r =self.request.post(upgradeUrlString, HttpEntityBuilder.create_string_entity(json.dumps(upgradeRequestBody)), contentType='application/json')
        if r.getStatus() not in HTTP_SUCCESS:
            self.throw_error(r)
        if self.getStateAfterTransitioning(service) == 'upgraded':
            print "Service %s has been upgraded\n" % service['id']
        else:
            print "Service %s has not been upgraded; do rollback\n" % service['id']

    # End upgradeRancherServices

    def getStateAfterTransitioning(self, service):
    #   print "Executing method getStateAfterTransitioning() in class RancherClient class in file RancherClient.py\n"
        serviceLink = service['links']['self']
        serviceUrlString = urlparse(serviceLink).path[1:]
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

    # End getStateAfterTransitioning

    def throw_error(self, response):
    #   print "Executing method throw_error() in class RancherClient in file RancherClient.py\n"
        print "Error from Rancher, HTTP Return: %s\n" % (response.getStatus())
        sys.exit(1)

    # End throw_error
        
# End RancherClient
