import boto3

s3 = boto3.client('s3')
bucket_name = "ap-covid-border-data-bucket"

# Create the bucket (region example: us-east-1)
response = s3.create_bucket(
    Bucket=bucket_name,
)

print(f"✅ S3 Bucket '{bucket_name}' created successfully.")





