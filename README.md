# xld-rancher-plugin

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

