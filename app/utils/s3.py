import boto3
import os
from datetime import datetime
s3_client = boto3.client('s3')
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
        # Simply return None or raise an exception if you don't want to provide access
        print("Access is not permitted to the file.")
        return None  # No URL is generated
    except Exception as e:
        print(f"Error: {e}")
        return None