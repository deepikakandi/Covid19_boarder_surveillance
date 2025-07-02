import json
import boto3
import csv
import psycopg2
import os
from io import StringIO
from datetime import datetime

# Read environment variables
db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
db_port = int(os.environ.get('DB_PORT', 5432))

def clean_date(date_str):
    if not date_str.strip():
        return None
    for fmt in ("%m/%d/%y", "%Y-%m-%d"):  # Try both common formats
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue
    return None  # If all formats fail


def clean_row(row):
    return {
        'Test_ID': row['Test_ID'],
        'Person_Name': row['Person_Name'],
        'Age': int(row['Age']) if row['Age'].strip() else None,
        'Gender': row['Gender'],
        'Phone_Number': row['Phone_Number'],
        'Test_Date': clean_date(row['Test_Date']),
        'Result_Date': clean_date(row['Result_Date']),
        'Result': row['Result'],
        'District': row['District'],
        'Border_Location': row['Border_Location'],
        'ICMR_Report_Link': row['ICMR_Report_Link'],
        'Quarantine_Start_Date': clean_date(row['Quarantine_Start_Date']),
        'Quarantine_End_Date': clean_date(row['Quarantine_End_Date']),
        'Status': row['Status']
    }

def lambda_handler(event, context):
    try:
        print("Lambda triggered.")
        s3 = boto3.client('s3')

        # Get bucket and file key from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        print(f"Reading file from bucket: {bucket}, key: {file_key}")

        # Read the CSV file from S3
        response = s3.get_object(Bucket=bucket, Key=file_key)
        content = response['Body'].read().decode('utf-8')
        print(f"✅ S3 file read complete. Size: {len(content)} bytes")

        reader = csv.DictReader(StringIO(content))
        print("CSV reader initialized.")

        # Connect to PostgreSQL
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            dbname=db_name,
            port=db_port
        )
        cursor = conn.cursor()
        print("✅ Connected to PostgreSQL.")
        print("Inserting rows into DB...")

        insert_query = """
        INSERT INTO covid_test_data (
            test_id, person_name, age, gender, phone_number, test_date,
            result_date, result, district, border_location, icmr_report_link,
            quarantine_start_date, quarantine_end_date, status
        ) VALUES (
            %(Test_ID)s, %(Person_Name)s, %(Age)s, %(Gender)s, %(Phone_Number)s,
            %(Test_Date)s, %(Result_Date)s, %(Result)s, %(District)s, %(Border_Location)s,
            %(ICMR_Report_Link)s, %(Quarantine_Start_Date)s, %(Quarantine_End_Date)s,
            %(Status)s
        )
        """

        row_count = 0
        for row in reader:
            cleaned = clean_row(row)
            cursor.execute(insert_query, cleaned)
            row_count += 1

        conn.commit()
        cursor.close()
        conn.close()

        return {
            'statusCode': 200,
            'body': f"✅ {file_key} processed and inserted {row_count} rows into PostgreSQL RDS."
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"❌ Failed to process file {file_key}: {str(e)}"
        }
