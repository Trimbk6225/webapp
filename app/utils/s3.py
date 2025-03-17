import boto3
import os
from datetime import datetime

s3_client = boto3.client('s3', region_name=os.getenv('AWS_REGION'))

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def upload_file_to_s3(file, file_name):
    try:
        s3_client.upload_fileobj(file, BUCKET_NAME, file_name)
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

def delete_file_from_s3(file_name):
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_name)
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

def get_file_url(file_name):
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_name},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        return url
    except Exception as e:
        print(f"Error generating URL: {e}")
        return None
