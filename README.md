# XL Deploy Rancher plugin #

## CI status ##

[![Build Status][xld-rancher-plugin-travis-image]][xld-rancher-plugin-travis-url]
[![License: MIT][xld-rancher-plugin-license-image]][xld-rancher-plugin-license-url]
![Github All Releases][xld-rancher-plugin-downloads-image]

[xld-rancher-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xld-rancher-plugin.svg?branch=master
[xld-rancher-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xld-rancher-plugin
[xld-rancher-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xld-rancher-plugin-license-url]: https://opensource.org/licenses/MIT
[xld-rancher-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xld-rancher-plugin/total.svg

### Configuring the CLI interface ###

Set up a rancher.RancherCliClient object with Rancher server URL, access key and secret key.

Configure an application stack as a a compose.zip file containing a docker-compose.yml file and a rancher-compose.yml file.  Create a rancher.ComposeArchive artifact from the compose.zip file.

![Screenshot of RancherCliClient](images/RancherCliClient.png)

### Configuring the REST interface ###

Define a rancher.RancherRestClient object in the Infrastructure tree.  It can be located under the root node or any folder.  Set the host (DNS or IP), port, access key, and secret key.

![Screenshot of RancherRestClient](images/RancherRestClient.png)


### Deploying ###

Deploy the rancher.ComposeArtifact to the rancher.RancherCliClient or the rancher.RancherRestClient in order to create, update, upgrade, or delete the corresponding object on Rancher.

To configure a rancher.ComposeArchive object for deployment:

* Include a zip file containing the docker-compose.yml and rancher-compose.yml files as the artifact.

* Specify the project and stack names.

* Enter the names of the services that should be upgraded under a NOOP deployment.

* Set the uniqueMatchOnly flag to true if the deployment should abort on multiple matches for the project and stack names.

![Screenshot of ComposeArchive](images/ComposeArchive.png)

##### Mapping of XL Deploy actions to Rancher actions #####

**CLI**

* CREATE -- implemented to create a stack

* MODIFY

* NOOP

* DESTROY

**REST**

* CREATE -- implemented to create a stack

* MODIFY

* NOOP  -- implemented to upgrade the listed services

* DESTROY

