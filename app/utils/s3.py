import time
import boto3
import os
from datetime import datetime
from app.utils.statsd_client import record_timer

s3_client = boto3.client('s3')
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def upload_file_to_s3(file, file_name, metadata=None):
    start_time = time.time()
    try:
       
        extra_args = {}
        if metadata:
            extra_args['Metadata'] = metadata 
        
       
        s3_client.upload_fileobj(file, BUCKET_NAME, file_name, ExtraArgs=extra_args)
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False
    
    finally:
        duration = time.time() - start_time
        record_timer("s3.upload.duration", duration)  
def delete_file_from_s3(file_name):
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_name)
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

def get_file_url(file_name):
    try:
       
        url = f"{BUCKET_NAME}/{file_name}"
        
        return url
    except Exception as e:
        print(f"Error generating URL: {e}")
        return None