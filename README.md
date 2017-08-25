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

##### Mapping of XL Deploy actions to Rancher actions #####

**CLI**

* CREATE -- implemented to create a stack

* MODIFY

* NOOP

* DESTROY

** REST **

* CREATE

* MODIFY

* NOOP  -- implemented to upgrade a service

* DESTROY

