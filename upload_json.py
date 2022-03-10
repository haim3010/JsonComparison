import logging
import boto3
from botocore.exceptions import ClientError
import json
import os

AWS_REGION = 'us-east-1'

ENDPOINT_URL = "http://10.5.0.5:4566/"
# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

# boto3.setup_default_session(profile_name=AWS_PROFILE)

s3_client = boto3.client("s3", region_name=AWS_REGION,
                         use_ssl=False,
                         endpoint_url=ENDPOINT_URL,
                         aws_access_key_id="test",
                         aws_secret_access_key="test")

def create_bucket(bucket_name):
    """
    Creates a S3 bucket.
    """
    try:
        response = s3_client.create_bucket(
            Bucket=bucket_name)
    except ClientError:
        logger.exception('Could not create S3 bucket locally.')
        raise
    else:
        return response


def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to a S3 bucket.
    """
    try:
        if object_name is None:
            object_name = os.path.basename(file_name)
        response = s3_client.upload_file(
            file_name, bucket, object_name)
    except ClientError:
        logger.exception('Could not upload file to S3 bucket.')
        raise
    else:
        return response


def main():
    """
    Main invocation function.
    """
    bucket_name = "localstack-bucket"
    logger.info('Creating S3 bucket locally using LocalStack...')
    s3 = create_bucket(bucket_name)
    logger.info('S3 bucket created.')
    logger.info(json.dumps(s3, indent=4) + '\n')

    file_name = './analyzer.json'
    object_name = 'analyzer.json'
    bucket = 'localstack-bucket'
    logger.info('Uploading file to S3 bucket in LocalStack...')
    s3 = upload_file(file_name, bucket, object_name)
    logger.info('File uploaded to S3 bucket successfully.')



    # print(s3_client.list_objects(Bucket='localstack-bucket')['Contents'])


if __name__ == '__main__':
    main()