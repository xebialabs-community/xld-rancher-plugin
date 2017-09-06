#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

print "Executing upgrade.py"

import sys
from rancher.rest.RancherClientUtil import RancherClientUtil

rancherClient = RancherClientUtil.createRancherClient(deployed.container)

projectList = rancherClient.lookupProjectByName(deployed.projectName)

rancherClient.validateListLength(projectList, deployed.uniqueMatchOnly)

for project in projectList:
  print "Target project id is %s\n" % project['id']
  stackList = rancherClient.lookupStackByName(project, deployed.stackName)

for stack in stackList:
  print "Target stack id is %s\n" % stack['id']
  servicesList = rancherClient.getStackServices(stack)
  for service in servicesList:
    if service['name'] in deployed.serviceNames:
    	print "Target service id is %s\n" % service['id']
    	rancherClient.upgradeService(service)

