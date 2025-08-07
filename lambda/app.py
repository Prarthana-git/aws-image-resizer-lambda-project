import boto3
from PIL import Image
import io
import os

s3 = boto3.client('s3')
destination_bucket = os.environ['DEST_BUCKET']

def lambda_handler(event, context):
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        try:
            # Get the image from the source bucket
            response = s3.get_object(Bucket=source_bucket, Key=key)
            image_content = response['Body'].read()

            # Open the image and resize it
            img = Image.open(io.BytesIO(image_content))
            img = img.resize((128, 128))  # Resize to 128x128 pixels

            # Save resized image to buffer
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG')
            buffer.seek(0)

            # Upload resized image to the destination bucket
            s3.put_object(Bucket=destination_bucket, Key=key, Body=buffer)

            print(f"Resized and uploaded: {key}")

        except Exception as e:
            print(f"Error processing {key}: {e}")

    return {
        'statusCode': 200,
        'body': 'Image processed.'
    }
