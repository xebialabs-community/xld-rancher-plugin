#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os
import sys
from zipfile import ZipFile

from rancher.rest.RancherClientUtil import RancherClientUtil

print "Executing create.py"

rancherClient = RancherClientUtil.createRancherClient(deployed.container)

composeZip = ZipFile(deployed.file.path)

with composeZip.open("docker-compose.yml") as dockerComposeFile:
  dockerCompose = dockerComposeFile.read()

with composeZip.open("rancher-compose.yml") as rancherComposeFile:
  rancherCompose = rancherComposeFile.read()

projectList = rancherClient.lookupProjectByName(deployed.projectName)

rancherClient.validateListLength(projectList, deployed.uniqueMatchOnly)

for project in projectList:
  print "Target project id is %s\n" % project['id']
  stack = rancherClient.createStack(project, deployed.stackName, dockerCompose, rancherCompose)
  rancherClient.activateServices(stack)

