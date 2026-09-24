from src.etl import extract, transform, save_cleaned, load
from src.s3 import upload_to_s3


def main():
    print("=" * 40)
    print("RESTAURANT SALES ETL PIPELINE")
    print("=" * 40)

    raw_data = extract()

    cleaned_data = transform(raw_data)

    save_cleaned(cleaned_data)

    # Upload raw CSV to S3
    upload_to_s3(
        "data/raw/restaurant_sales.csv",
        "raw/restaurant_sales.csv"
    )

    # Upload cleaned CSV to S3
    upload_to_s3(
        "data/processed/cleaned_restaurant_sales.csv",
        "cleaned/cleaned_restaurant_sales.csv"
    )

    # Load cleaned data into PostgreSQL
    load(cleaned_data)

    print("=" * 40)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 40)


if __name__ == "__main__":
    main()