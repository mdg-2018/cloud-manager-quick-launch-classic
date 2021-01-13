# MongoDB Ops/Cloud Manager Automation Example
An example for automating the deployment of new MongoDB replica sets using AWS, Ansible, and the Cloud/Ops Manager API

## Getting Started

### Step 1: Edit configs
To get started using this script, edit the <code>deploymentConfig.json</code> file. Fill out the following fields:

<code>"projectID"</code> - This is the Cloud Manager / Ops Manager project id. You can get it from the project settings page.<br>
<code>"apiPublicKey"</code> - When you create an API key for Cloud Manager / Ops Manager, you will get a public and private key. Details on getting these keys are available in the documentation [here](https://docs.cloudmanager.mongodb.com/tutorial/configure-public-api-access/).<br>
<code>"apiPrivateKey"</code> - See above.<br>
<code>"rootURL"</code> - This is the root url for either Cloud Manager or Ops Manager. If you're using Cloud Manager it will be https://cloud.mongodb.com. If you're using Ops Manager it will vary based on your deployment.<br>
<code>"mmsGroupId"</code> - ID for the Cloud Manager / Ops Manager project we're working with.<br>
<code>"mmsApiKey"</code> - This is the API key for the Cloud Manager / Ops Manager agents. You can find this info [here](https://docs.cloudmanager.mongodb.com/tutorial/manage-agent-api-key/).<br>
<code>"ansible_ssh_private_key_file"</code> - This is the path to your .pem key file to be able to access your EC2 instances in AWS<br>

### Step 2: Install dependencies.
Make sure Ansible and Python 3 are installed.

### Step 3: Configure AWS api keys
Make sure your AWS credentials are stored in <code>~/.aws/credentials</code>. It should look something like this:<br>
<code>[ProfileName]
<br>aws_access_key_id = SomeRandomString<br>
aws_secret_access_key = SomeOtherRandomString</code>

### Step 4: Set up Ops Manager / Cloud Manager project
Make sure you create a user so you can connect to the replica set. Also, enable TLS on the security page. The CA File Path should be /etc/ssl/certs/mdbserverCA.pem. I like to set Client Certificate Mode to REQUIRE but this is up to you!

### Step 5: Run the ansible playbook!
Run <code>ansible-playbook playbook.yaml</code> in the terminal. Once the playbook has finished it should spit out a connection string and the key files you need to connect to the cluster in the <code>connections</code> directory.