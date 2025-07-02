CREATE TABLE covid_test_data (
    test_id UUID PRIMARY KEY,
    person_name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    phone_number VARCHAR(20),
    test_date DATE,
    result_date DATE,
    result VARCHAR(10),
    district VARCHAR(100),
    border_location VARCHAR(100),
    icmr_report_link TEXT,
    quarantine_start_date DATE,
    quarantine_end_date DATE,
    status VARCHAR(20)
);

