import boto3
from botocore.exceptions import ClientError
import re
import sys

s3 = boto3.resource('s3')
try:
    client = boto3.client('s3')
except ClientError as e:
    # Couldn't connect to AWS
    print("AWS API couldn't connect. exiting.")
    sys.exit(1)

r = re.compile('^tcat.*$')
task_cat_buckets = [b['Name'] for b in client.list_buckets()['Buckets'] if r.match(b['Name'])]
for bucket in task_cat_buckets:
  # must first delete contents of bucket before we can delete bucket
  s3.Bucket(bucket).objects.all().delete()
  s3.Bucket(bucket).delete()
