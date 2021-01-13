#!/bin/python3
import requests
import json
from requests.auth import HTTPDigestAuth
import sys
import os.path

# import config file
deploymentConfig = json.load(open('deploymentConfig.json'))

projectID = deploymentConfig['projectID']

# build list of servers
servers = sys.argv
servers.pop(0)
servers = servers[0].replace("[","")
servers = servers.replace("]","")
servers = servers.replace("'","")
servers = servers.replace("\"","")
servers = servers.replace("\n","")
servers = servers.replace(" ","")
servers = servers.replace(", ",",")
servers = servers.split(",")

# get current automation config
rootURL = deploymentConfig['rootURL']
URL = rootURL + "/api/public/v1.0/groups/" + projectID + "/automationConfig"
automationConfig = requests.get(URL, auth=HTTPDigestAuth(
    deploymentConfig['apiPublicKey'], deploymentConfig['apiPrivateKey']))
newConfig = automationConfig.json()

# add monitoring and backup to each server
for server in servers:
  newMonitoringAgent = {"hostname": server}
  newBackupAgent = {"hostname": server}
  newConfig['monitoringVersions'].append(newMonitoringAgent)
  newConfig['backupVersions'].append(newBackupAgent)

# replica set
newRSName = "rs" + str(len(newConfig['replicaSets']) + 1)

newRS = {
    "_id": newRSName,
    "protocolVersion":"1",
    "members": []
}

nodeCounter = len(newConfig['replicaSets']) * 100
for server in servers:
    # add rs members
    newRS['members'].append({
        "_id":nodeCounter,
        "host": server,
        "priority": 1,
        "votes": 1,
        "slaveDelay": 0,
        "hidden": False,
        "arbiterOnly": False
      })

    # add mongod processes
    newConfig['processes'].append({
    "version": "4.4.1-ent",
    "name": server,
    "hostname": server,
    "logRotate": {
      "sizeThresholdMB": 1000,
      "timeThresholdHrs": 24
    },
    "authSchemaVersion": 5,
    "featureCompatibilityVersion": "4.4",
    "processType": "mongod",
    "args2_6": {
      "net": {
        "port": 27017,
        "tls":{
            "mode":"requireTLS",
            "certificateKeyFile":"/etc/ssl/certs/mdbserver.pem"
        }
      },
      "storage": {
        "dbPath": "/data/" + newRSName
      },
      "systemLog": {
        "path": "/data/" + newRSName + "/mongodb.log",
        "destination": "file"
      },
      "replication": {
        "replSetName": newRSName
      }
    }
    })
    nodeCounter+=1
  
newConfig['replicaSets'].append(newRS)

# set tls configuration
newConfig['tls']['CAFilePath'] = "/etc/ssl/certs/mdbserverCA.pem"
newConfig['tls']['clientCertificateMode'] = "REQUIRE"

result = requests.put(URL,data=json.dumps(newConfig),headers={"Content-Type":"application/json"},auth=HTTPDigestAuth(deploymentConfig['apiPublicKey'], deploymentConfig['apiPrivateKey']))

# create connection string
connString="mongodb://username:password@"
svrCounter=1
for server in servers:
  connString+= server
  if svrCounter != len(servers):
    connString+= ","
  svrCounter+=1

connString+= "/admin?replicaSet=" + newRS['_id']

print(result.text)

print(connString)
