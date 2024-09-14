import boto3
from botocore.exceptions import ClientError
import os

class StorageProvider:
    def __init__(self):
        self.client = boto3.client('s3',
                                   endpoint_url=os.getenv('DO_SPACES_ENDPOINT'),
                                   aws_access_key_id=os.getenv('DO_SPACES_KEY'),
                                   aws_secret_access_key=os.getenv('DO_SPACES_SECRET'))
        self.bucket = os.getenv('DO_SPACES_BUCKET')

    def upload_fileobj(self, file_obj, object_name):
        try:
            self.client.upload_fileobj(file_obj, self.bucket, object_name)
        except ClientError as e:
            print(f"Error uploading file object: {e}")
            return None

        return f"{os.getenv('DO_SPACES_ENDPOINT')}/{self.bucket}/{object_name}"

    def delete_file(self, file_url):
        object_name = file_url.split('/')[-1]
        try:
            self.client.delete_object(Bucket=self.bucket, Key=object_name)
        except ClientError as e:
            print(f"Error deleting file: {e}")

    def get_total_size(self):
        try:
            response = self.client.list_objects_v2(Bucket=self.bucket)
            return sum(obj['Size'] for obj in response.get('Contents', []))
        except ClientError as e:
            print(f"Error getting total size: {e}")
            return 0