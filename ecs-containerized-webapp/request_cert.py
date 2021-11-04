#!/usr/bin/env python
import boto3
from botocore.exceptions import ClientError
import sys

# The hosted zone in Route53
hosted_zone_name = sys.argv[1]
# domain name for SSL cert, use "*" to protect against multiple subdomains
cert_domain_name = "*."+hosted_zone_name
# Idempotency Token to prevent requesting multiple SSL certs
idem_token = '12345'

try:
    route53 = boto3.client('route53')
    acm = boto3.client('acm')
except ClientError as e:
    print("Couldn't connect")
    print(e)
    sys.exit(1)

# Request SSL Certificate
response = acm.request_certificate(DomainName=cert_domain_name, ValidationMethod='DNS',
                                   IdempotencyToken=idem_token)
cert_arn = response['CertificateArn']
response = acm.describe_certificate(CertificateArn=cert_arn)

cname_source = response['Certificate']['DomainValidationOptions'][0]['ResourceRecord']['Name']
cname_value = response['Certificate']['DomainValidationOptions'][0]['ResourceRecord']['Value']

# Create DNS record for Certificate Validation
response = route53.list_hosted_zones_by_name(DNSName=hosted_zone_name)
hosted_zone_id = response['HostedZones'][0]['Id']
response = route53.change_resource_record_sets(HostedZoneId=hosted_zone_id,
                                               ChangeBatch={'Comment': 'alias %s -> %s' % (cname_source, cname_value),
                                                            'Changes': [
                                                   {
                                                       'Action': 'UPSERT',
                                                       'ResourceRecordSet': {
                                                           'Name': cname_source,
                                                           'Type': 'CNAME',
                                                           'TTL': 300,
                                                           'ResourceRecords': [{'Value': cname_value}]
                                                       }
                                                   }]
                                               })

# Finally, print Certificate ARN back into bash script
print(cert_arn)
