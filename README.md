# 🦠 COVID-19 Border Testing Automation & Analytics Project (Andhra Pradesh, India)

This project simulates a real-world solution built for the **Andhra Pradesh state government** to monitor COVID-19 testing at **border entry points**. It involves collecting test data, storing it in AWS RDS, automating daily report generation, notifying officials, performing exploratory data analysis, and predicting quarantine recovery using ML.

---

## 🚀 Project Highlights

- 🔄 **Automated pipeline**: S3 ➜ Lambda ➜ PostgreSQL (RDS)
- 📈 **Exploratory Data Analysis (EDA)** in Pandas + Tableau
- 📤 **Daily Reports** generated and uploaded to S3
- 📨 **Notifications** to stakeholders via Amazon SNS
- 🤖 **Machine Learning** model to predict quarantine duration
- 🔐 **Secure pipeline**: S3 encryption, IAM auth, Secrets Manager

---

## 📂 Folder Structure

📦covid19-border-surveillance
┣ 📁etl-lambda/
┃ ┗ lambda_function.py # Lambda to insert data from S3 to RDS
┣ 📁report-lambda/
┃ ┗ daily_report_lambda.py # Lambda to generate daily report & notify
┣ 📁eda/
┃ ┗ covid_eda.ipynb # Jupyter notebook for data analysis
┣ 📁ml/
┃ ┗ quarantine_predictor.py # ML model to predict recovery duration
┣ 📁data/
┃ ┗ Covid_batch_sample.csv # Sample input dataset (50k+ records)
┗ 📄 README.md


## 🔧 Tech Stack

| Layer         | Service/Tool         |
|---------------|----------------------|
| Data Storage  | Amazon RDS (PostgreSQL) |
| File Storage  | Amazon S3            |
| Compute       | AWS Lambda           |
| Scheduler     | Amazon EventBridge   |
| Notification  | Amazon SNS           |
| Secrets Mgmt  | AWS Secrets Manager  |
| ML/EDA        | Python, Pandas, Scikit-learn |
| Visualization | Tableau              |

---

**Lambda Functions**

**etl-lambda: CSV Upload to RDS**

1. Triggered when new .csv file is uploaded to S3:/uploads/

2. Reads file → parses rows → inserts into PostgreSQL RDS

**report-lambda: Daily Report + Notification**

1. Scheduled using EventBridge (cron(0 8 * * ? *))

2. Queries data for current date

3. Generates Excel report using pandas + xlsxwriter

4. Uploads to S3 under /daily-reports/yyyy-mm-dd/

5. Sends SNS email with public report link

**Exploratory Data Analysis**

1. Jupyter notebook explores:

2. Test result trends (daily/weekly)

3. District-wise positive rate

4. Quarantine delay and duration

5. Gender/Age group analysis

6. Border hotspots


**ML Model: Quarantine Recovery Predictor**

1. Trains LinearRegression on age/gender → predicts quarantine_days

2. Can be deployed in a separate prediction Lambda or used in offline analysis


**Automation**

1. Task	Service
2. Data Ingestion	Lambda + S3
3. Scheduling	EventBridge
4. Notifications	SNS Email
5. Secrets Management	AWS Secrets Manager
6. Bucket Security	SSE-S3 / SSE-KMS
7. RDS Authentication	IAM + Encrypted

**Deployment Notes**

1. Upload .csv to S3:/uploads/ ➜ triggers ETL Lambda

2. Daily at 8 AM:

3. Report is generated from RDS

4. Uploaded to S3:/daily-reports/yyyy-mm-dd/

5. Email is sent to collector team

**Security**

1. S3: Server-side encryption enabled

2. RDS: IAM authentication, multi-AZ, backups

3. Lambda: Uses Secrets Manager for DB credentials

4. IAM: Scoped permissions to limit access

**Dashboard (Tableau)**

1. Total Tests, Positives, Positivity Rate, Active Cases

2. Trends over time by district, gender, age group

3. Border hotspot map

4. Average quarantine duration

**Getting Started (Local Testing)**

  # Install requirements
  pip install -r requirements.txt
  
  # Run ML model manually
  python ml/quarantine_predictor.py
  
  # Run EDA notebook
  jupyter notebook eda/covid_eda.ipynb


**🤝 Credits**
Developed by Deepika Kandi – for portfolio purposes, inspired by real-world public health tech.

**contact:**
**LinkedIn : www.linkedin.com/in/deepika-kandi**
**E-mail: kandideepika3@gmail.com**

