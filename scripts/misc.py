import boto3
from botocore.exceptions import ClientError
import logging
import re
import sys

class S3():
    def __init__(self):
        self.s3 = boto3.resource('s3')
        try:
            self.client = boto3.client('s3')
        except ClientError as e:
            logging.error(e)
            # Couldn't connect to AWS
            print("AWS API couldn't connect. exiting.")
            sys.exit(1)

    def list_buckets(self, regex=".*", verbose=False):
        """Add regex filter for list_buckets

        verbose: boolean
            if verbose is false, only the bucket names will be returned. If
            true, all bucket information will be returned.
        """
        r = re.compile(regex)
        if verbose:
            return [b for b in self.client.list_buckets()['Buckets'] if r.match(b['Name'])]
        else:
            return [b['Name'] for b in self.client.list_buckets()['Buckets'] if r.match(b['Name'])]

    def list_objects(self, bucket_name):
        return self.client.Bucket(name=bucket_name).objects.all()

    def rm_buckets(self, buckets, force=False):
        """Deletes an empty S3 bucket. If the force boolean is
        set to True, the contents of the Bucket will first be
        deleted before deleting the bucket.

        force: boolean
        """
        if type(buckets) is list:
            for bucket in buckets:
                if force:
                    # Delete contents in buckets
                    self.s3.Bucket(bucket).objects.all().delete()
                self.s3.Bucket(bucket).delete()
        else:
            if force:
                # rm contents in bucket
                self.s3.Bucket(buckets).objects.all().delete()
            self.s3.Bucket(buckets).delete()

    # def create_bucket(self, bucketname, acl='private'):
    #     acls = ('private', 'public-read', 'public-read-write')
    #     locations =
    #     bucket = self.s3.Bucket(bucketname)
    #     response = bucket.create(ACL=acl)
    #     return response

class ManagedCert():

    def __init__(self):
        #self.acm = boto3.resource('acm')
        try:
            self.client = boto3.client('acm')
        except ClientError as e:
            logging.error(e)
            # Couldn't connect to AWS
            print("AWS API couldn't connect. exiting.")
            sys.exit(1)


    def request_cert(self, domain_name):
        response = self.client.request_certificate(DomainName=domain_name,
                ValidationMethod='DNS')
        return response

    def list_certs(self):
        response = self.client.list_certificates()
        return response
