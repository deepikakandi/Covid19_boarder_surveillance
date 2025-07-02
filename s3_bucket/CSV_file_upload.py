import boto3

s3 = boto3.client('s3')
bucket_name = "ap-covid-border-data-bucket"
file_path = "covid_border_testing_ap.csv"
object_name = "raw_data/covid_border_testing_ap.csv"

# Upload file
s3.upload_file(file_path, bucket_name, object_name)

print(f"✅ File uploaded to S3 at s3://{bucket_name}/{object_name}")


