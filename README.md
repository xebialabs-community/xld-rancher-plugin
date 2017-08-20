# xld-rancher-plugin

Configuration

Set up a rancher.rancherClient object with Rancher server URL, access key and secret key.

Configure an application stack as a a compose.zip file containing a docker-compose.yml file and a rancher-compose.yml file.  Create a rancher.ComposeArchive artifact from the compose.zip file.

Deploy the rancher.ComposeArtifact to the rancher.rancherClient in order to create the application stack on Rancher.
