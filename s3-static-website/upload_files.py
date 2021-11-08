#!/usr/bin/env python
import boto3
from botocore.exceptions import ClientError
import sys
import os
import logging
from pathlib import Path

bucket = sys.argv[1]
src_dir = sys.argv[2]

def upload_file(file_name, bucket, object_name=None, ExtraArgs={'ContentType':'text/html'}):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=ExtraArgs)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    for path in Path(src_dir).rglob('*'):
        if path.is_file():
            filename = path.relative_to(src_dir)
            filename = str(filename)
            path = str(path)
            if filename.endswith('html'):
                ExtraArgs = {'ContentType': 'text/html'}
            elif filename.endswith('css'):
                ExtraArgs = {'ContentType': 'text/css'}
            elif filename.endswith('png'):
                ExtraArgs = {'ContentType': 'image/png'}
            elif filename.endswith('jpeg') or filename.endswith('jpg'):
                ExtraArgs = {'ContentType': 'image/jpeg'}
            upload_file(path, bucket, filename, ExtraArgs=ExtraArgs)
