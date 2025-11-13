import boto3
from botocore.exceptions import NoCredentialsError
from app.utils.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME
from datetime import datetime

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

async def upload_image_to_s3(file_bytes: bytes, filename: str, folder: str = "students") -> str:
    """
    Upload an image to AWS S3 and return the public URL.
    """
    try:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        key = f"{folder}/{timestamp}_{filename}"

        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=key,
            Body=file_bytes,
            ContentType="image/jpeg",
            ACL="public-read"
        )

        return f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"

    except NoCredentialsError:
        raise Exception("AWS credentials not configured properly.")


async def delete_image_from_s3(file_url: str) -> bool:
    """
    Delete an image from AWS S3 using its URL.
    """
    try:
        key = file_url.split(f"{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/")[-1]
        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=key)
        return True
    except Exception:
        return False
