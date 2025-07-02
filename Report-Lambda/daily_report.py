import boto3
import psycopg2
import pandas as pd
import datetime
import os

def lambda_handler(event, context):
    # 1. Connect to PostgreSQL
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        dbname=os.environ['DB_NAME'],
        port=os.environ.get('DB_PORT', 5432)
    )
    # 2. Query data
    df = pd.read_sql("""
        SELECT * FROM covid_test_data
        WHERE test_date = CURRENT_DATE
    """, conn)
    conn.close()

    # 3. Generate Excel report
    today = datetime.date.today().isoformat()
    file_name = f"covid_report_{today}.xlsx"
    s3_key = f"daily-reports/{today}/{file_name}"
    df.to_excel(f"/tmp/{file_name}", index=False)

    # 4. Upload to S3
    s3 = boto3.client('s3')
    s3.upload_file(f"/tmp/{file_name}", os.environ['REPORT_BUCKET'], s3_key)

    return {"statusCode": 200, "body": f"Report generated and uploaded to S3://{os.environ['REPORT_BUCKET']}/{s3_key}"}
