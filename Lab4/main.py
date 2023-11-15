import requests
import subprocess

from os import popen
from json import loads

from time import sleep

def getCurrentAccessToken():
    stream = popen('az account get-access-token --resource=https://management.azure.com')
    output = loads(stream.read())

    return output.get('accessToken')

authorization_token = getCurrentAccessToken()

headers = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {authorization_token}'
}

request_data = [
    { # Resource Groups - Create or Update
        'url': "https://management.azure.com/subscriptions/95a550e5-ba68-4d4f-ab19-9ece4738f45f/resourcegroups/lab4?api-version=2021-04-01",
        'body': {
            'location': "westeurope"
        }
    },
    { # Virtual Network - Create or Update
        'url': "https://management.azure.com/subscriptions/95a550e5-ba68-4d4f-ab19-9ece4738f45f/resourceGroups/lab4/providers/Microsoft.Network/virtualNetworks/net4?api-version=2023-05-01",
        'body': {
            "properties": {
                "addressSpace": {
                    "addressPrefixes": [
                        "10.0.0.0/16"
                    ]
                },
                "flowTimeoutInMinutes": 10
            },
            "location": "westeurope"
        }
    },
    { # Subnets - Create Or Update
        'url': "https://management.azure.com/subscriptions/95a550e5-ba68-4d4f-ab19-9ece4738f45f/resourceGroups/lab4/providers/Microsoft.Network/virtualNetworks/net4/subnets/snet4?api-version=2023-05-01",
        'body':  {
            "properties": {
                "addressPrefix": "10.0.0.0/16"
            }
        }
    },
    { # Public IP Addresses - Create Or Update
        'url': "https://management.azure.com/subscriptions/95a550e5-ba68-4d4f-ab19-9ece4738f45f/resourceGroups/lab4/providers/Microsoft.Network/publicIPAddresses/ip4?api-version=2023-05-01",
        'body': {
            "location": "westeurope"
        }
    },
    { # Network Interfaces - Create Or Update
        'url': "https://management.azure.com/subscriptions/95a550e5-ba68-4d4f-ab19-9ece4738f45f/resourceGroups/lab4/providers/Microsoft.Network/networkInterfaces/nic4?api-version=2023-05-01",
        'body': {
            "properties": {
                "ipConfigurations": [
                    {
                        "name": "ipconfig1",
                        "properties": {
                            "publicIPAddress": {
                                "id": "/subscriptions/95a550e5-ba68-4d4f-ab19-9ece4738f45f/resourceGroups/lab4/ providers/Microsoft.Network/publicIPAddresses/ip4"
                            },
                            "subnet": {
                                "id": "/subscriptions/95a550e5-ba68-4d4f-ab19-9ece4738f45f/resourceGroups/lab4/ providers/Microsoft.Network/virtualNetworks/net4/subnets/snet4"
                            }
                        }
                    }
                ]
            },
            "location": "westeurope"
        }
    },
    { # Virtual Machines - Create Or Update
        'url': "https://management.azure.com/subscriptions/95a550e5-ba68-4d4f-ab19-9ece4738f45f/resourceGroups/lab4/providers/Microsoft.Compute/virtualMachines/vm4?api-version=2023-07-01",
        'body': {
            "id": "/subscriptions/95a550e5-ba68-4d4f-ab19-9ece4738f45f/resourceGroups/lab4/ providers/Microsoft.Compute/virtualMachines/vm4",
            "type": "Microsoft.Compute/virtualMachines",
            "properties": {
                "osProfile": {
                    "adminUsername": "paul",
                    "secrets": [
                        
                    ],
                    "computerName": "vm4",
                    "linuxConfiguration": {
                        "ssh": {
                        "publicKeys": [
                            {
                                "path": "/home/paul/.ssh/authorized_keys",
                                "keyData": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCsxP2gmr2VhefmSeB07WtVpOP3IquuVmGgx23jjW7i hA+rJjsUnEA/ uf5a9Qr5tvA3fDlaADTKOn8A54j2KVut1My4soro4YL5ziyiIYjzcn9CCI7EUscB41f1vNQqGuhvJot2 UB4mKRLDgJgtCUzM5jm5Su32yJQa1Zybl9uxyU/ BFnK3JFiynoMl30ADbZYBz6owc4+yFJDy46l0SiAiOJRKlPQmrH10YMnWQyiFrON07b2RJRyPr80 QXt9t+ynWGwJeO5nv1WQZirNVuzze1yWCQtQ8L3ySFSj9LA3Xw2n34NEWUvK6PMGmJf1+Fnx jVzC6KxExKkglXXfcv8N9 paul@paul "
                            }
                        ]
                        },
                        "disablePasswordAuthentication": True
                    }
                    },
                    "networkProfile": {
                        "networkInterfaces": [
                            {
                                "id": "/subscriptions/95a550e5-ba68-4d4f-ab19-9ece4738f45f/resourceGroups/lab4/ providers/Microsoft.Network/networkInterfaces/nic4",
                                "properties": {
                                    "primary": True
                                }
                            }
                        ]
                    },
                    "storageProfile": {
                        "imageReference": {
                            "sku": "16.04-LTS",
                            "publisher": "Canonical",
                            "version": "latest",
                            "offer": "UbuntuServer"
                        },
                        "dataDisks": [
                            
                        ]
                    },
                    "hardwareProfile": {
                    "vmSize": "Standard_D1_v2"
                },
                "provisioningState": "Creating"
            },
            "name": "vm4",
            "location": "westeurope"
        }
    },
]

for data in request_data:
    url = data.get('url')
    body = data.get('body')
        
    print(data)
    x = requests.put(url, headers=headers, json = body)
    sleep(5)
    print(x)