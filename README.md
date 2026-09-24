# Restaurant Sales ETL Pipeline

## Project Overview

This project implements an ETL (Extract, Transform, Load) pipeline for restaurant sales data using Python, Pandas, PostgreSQL, and Amazon S3.

The pipeline extracts raw sales data from a CSV file, cleans and validates the records, removes duplicates, logs rejected records, stores the cleaned dataset, uploads raw and cleaned data to Amazon S3, and loads valid records into PostgreSQL for analytical queries.

## Technologies Used

* Python
* Pandas
* PostgreSQL
* Amazon S3
* Boto3
* psycopg2
* SQL
* Git and GitHub

## Project Structure

```text
data-engineering-etl/
├── data/
│   ├── raw/
│   └── processed/
├── logs/
├── src/
│   ├── database.py
│   ├── etl.py
│   ├── generate_data.py
│   └── s3.py
├── sql/
│   ├── schema.sql
│   └── analysis.sql
├── .env.example
├── .gitignore
├── requirements.txt
├── run_pipeline.py
└── README.md
```

## ETL Workflow

```text
Raw CSV
   ↓
Extract
   ↓
Clean and Standardize
   ↓
Validate
   ↓
Remove Duplicates
   ↓
Rejected Records → logs/rejected_records.csv
   ↓
Cleaned CSV
   ↓
PostgreSQL
```

The pipeline also integrates with Amazon S3:

```text
Raw CSV
   ↓
S3 raw/restaurant_sales.csv

Cleaned CSV
   ↓
S3 cleaned/cleaned_restaurant_sales.csv
```

## Dataset

The generated dataset contains 10,520 raw records.

The dataset includes:

* Transaction information
* Customer names
* Restaurant names
* Categories
* Countries
* Quantities
* Unit prices
* Ratings
* Transaction dates

The raw dataset intentionally contains missing values, inconsistent text formatting, invalid numeric values, and duplicate records to demonstrate data cleaning and validation.

## Data Cleaning and Validation

The ETL pipeline performs the following operations:

* Removes duplicate transaction IDs
* Handles missing customer names
* Handles missing country values
* Standardizes text casing
* Removes unnecessary whitespace
* Converts numeric fields to appropriate data types
* Converts transaction dates to date format
* Validates positive quantities
* Validates positive unit prices
* Validates ratings between 1 and 5
* Logs rejected records

The pipeline produced:

* 10,520 raw records
* 3 rejected records
* 10,497 valid records

## PostgreSQL

The PostgreSQL database is named `restaurant_etl`.

The `restaurant_sales` table contains:

* Primary key on `transaction_id`
* NOT NULL constraints
* Quantity validation
* Unit price validation
* Rating range validation
* Indexes on country, category, transaction date, and restaurant

## Analytical Queries

The project includes three analytical SQL queries:

1. Top 10 restaurants by total revenue
2. Monthly revenue
3. Average rating by country

`EXPLAIN ANALYZE` is also used to inspect query execution plans and execution time.

## AWS S3

Amazon S3 is used to store both raw and cleaned datasets.

```text
restaurant-etl-nethmi-2026/
├── raw/
│   └── restaurant_sales.csv
└── cleaned/
    └── cleaned_restaurant_sales.csv
```

The Python pipeline uploads these files automatically using Boto3.

## Security

AWS and PostgreSQL credentials are stored in environment variables.

The `.env` file is excluded from Git using `.gitignore`.

A `.env.example` file is provided with placeholder values for configuration.

The AWS IAM user is granted only the S3 permissions required by the ETL pipeline.

## Scalability

For larger datasets containing millions of records, the pipeline can be improved by processing CSV files in chunks instead of loading the entire dataset into memory.

For example, Pandas can process data using a defined chunk size.

PostgreSQL scalability can be improved using:

* Batch inserts
* Indexing
* Table partitioning
* Connection pooling
* Query optimization

The pipeline can also be scheduled using tools such as cron or Apache Airflow.

For failure handling, database transactions can be rolled back when loading fails, while errors can be logged and failed tasks can be retried.

## Running the Pipeline

Activate the virtual environment and run:

```bash
python run_pipeline.py
```

The pipeline performs:

1. Data extraction
2. Data cleaning
3. Data validation
4. Duplicate removal
5. Rejected record logging
6. Cleaned CSV generation
7. S3 upload
8. PostgreSQL loading

## Configuration

Create a `.env` file using `.env.example` as a template and provide the required PostgreSQL and AWS configuration values.

Never commit the `.env` file or AWS credentials to GitHub.
