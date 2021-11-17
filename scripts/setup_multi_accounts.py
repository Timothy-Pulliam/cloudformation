#!/usr/bin/env python

import boto3

client = boto3.client('organizations')

root_id = client.list_roots()['Roots'][0]['Id']

ous = ('Security', 'Infrastructure', 'Sandbox', 'Workloads', 'Policy Staging', 
        'Suspended', 'Individual Business Users', 'Exceptions', 'Deployments')

for ou in ous:
    response = client.create_organizational_unit(ParentId=root_id, Name=ou)
    ou_id = response['OrganizationalUnit']['Id']
    ou_name = response['OrganizationalUnit']['Name']
    # Create prod/preprod sub ous
    if ou_name not in ('Sandbox', 'Policy Staging', 'Suspended', 'Exceptions',
            'Individual Business Users'):
        client.create_organizational_unit(ParentId=ou_id, Name="Prod")
        client.create_organizational_unit(ParentId=ou_id, Name="Pre-Prod")
