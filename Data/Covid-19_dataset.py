import pandas as pd
import random
import uuid
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)

districts = ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore', 'Tirupati', 'Anantapur', 'Kurnool', 'Chittoor']
border_checkposts = ['Ichchapuram', 'Palamaner', 'Kurnool Gate', 'Nellore NH16', 'Srikakulam Border', 'Chilakaluripet Entry']

def generate_covid_data(num_records=50000):
    data = []

    start_date = datetime.strptime('2021-01-01', '%Y-%m-%d').date()
    end_date = datetime.strptime('2021-06-30', '%Y-%m-%d').date()

    for _ in range(num_records):
        test_id = str(uuid.uuid4())
        name = fake.name()
        age = random.randint(1, 90)
        gender = random.choice(['Male', 'Female'])
        phone = fake.phone_number()
        test_date = fake.date_between(start_date=start_date, end_date=end_date)
        result_delay = random.randint(1, 3)
        result_date = test_date + timedelta(days=result_delay)
        result = random.choices(['Negative', 'Positive'], weights=[80, 20])[0]
        district = random.choice(districts)
        border = random.choice(border_checkposts)
        icmr_link = f"https://icmr.gov.in/reports/{test_id}.pdf"

        quarantine_start = result_date if result == 'Positive' else None
        quarantine_days = random.randint(14, 28)
        quarantine_end = quarantine_start + timedelta(days=quarantine_days) if quarantine_start else None
        status = 'Recovered' if result == 'Positive' and quarantine_end < datetime(2021, 7, 15).date() else ('Active' if result == 'Positive' else None)


        data.append({
            'Test_ID': test_id,
            'Person_Name': name,
            'Age': age,
            'Gender': gender,
            'Phone_Number': phone,
            'Test_Date': test_date,
            'Result_Date': result_date,
            'Result': result,
            'District': district,
            'Border_Location': border,
            'ICMR_Report_Link': icmr_link,
            'Quarantine_Start_Date': quarantine_start,
            'Quarantine_End_Date': quarantine_end,
            'Status': status
        })

    df = pd.DataFrame(data)
    return df

# Generate and save the data
df_covid = generate_covid_data(50000)
df_covid.to_csv('covid_border_testing_ap.csv', index=False)
print("✅ Dataset generated and saved as 'covid_border_testing_ap.csv'")
