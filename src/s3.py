import os
import boto3
from dotenv import load_dotenv

load_dotenv()


def upload_to_s3(file_path, s3_key):
    """Upload a file to an Amazon S3 bucket."""

    s3 = boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION")
    )

    bucket = os.getenv("S3_BUCKET_NAME")

    s3.upload_file(
        file_path,
        bucket,
        s3_key
    )

    print(f"Uploaded {file_path} to S3/{s3_key}")