import os
import pandas as pd

from src.database import get_connection


RAW_FILE = "data/raw/restaurant_sales.csv"
CLEAN_FILE = "data/processed/cleaned_restaurant_sales.csv"
REJECTED_FILE = "logs/rejected_records.csv"


def extract():
    """Read the raw CSV dataset."""
    print("Extracting raw data...")

    df = pd.read_csv(RAW_FILE)

    print(f"Records extracted: {len(df)}")
    return df


def transform(df):
    """Clean, standardize, and validate the data."""
    print("Cleaning and validating data...")

    # Remove duplicate transaction IDs, keeping the first occurrence.
    df = df.drop_duplicates(subset=["transaction_id"], keep="first").copy()

    # Standardize text fields and handle missing values.
    df["customer_name"] = (
        df["customer_name"].fillna("Unknown").astype(str).str.strip()
    )

    df["restaurant"] = df["restaurant"].fillna("").astype(str).str.strip().str.title()
    df["category"] = df["category"].fillna("").astype(str).str.strip().str.title()
    df["country"] = (
        df["country"].fillna("Unknown").astype(str).str.strip().str.title()
    )

    # Convert numeric fields; invalid values become missing.
    for column in ["transaction_id", "quantity", "unit_price", "rating"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Convert dates; invalid dates become missing.
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"], errors="coerce"
    )

    # Identify records that fail validation.
    valid_mask = (
        df["transaction_id"].notna()
        & (df["transaction_id"] % 1 == 0)
        & (df["restaurant"] != "")
        & (df["category"] != "")
        & (df["country"] != "")
        & df["quantity"].notna()
        & (df["quantity"] > 0)
        & (df["quantity"] % 1 == 0)
        & df["unit_price"].notna()
        & (df["unit_price"] > 0)
        & df["rating"].notna()
        & df["rating"].between(1, 5)
        & df["transaction_date"].notna()
    )

    rejected = df.loc[~valid_mask].copy()
    cleaned = df.loc[valid_mask].copy()

    # Save rejected records for review.
    os.makedirs("logs", exist_ok=True)
    rejected.to_csv(REJECTED_FILE, index=False)

    # Convert values to suitable types for PostgreSQL.
    cleaned["transaction_id"] = cleaned["transaction_id"].astype(int)
    cleaned["quantity"] = cleaned["quantity"].astype(int)
    cleaned["transaction_date"] = cleaned["transaction_date"].dt.date

    print(f"Rejected records: {len(rejected)}")
    print(f"Valid records: {len(cleaned)}")

    return cleaned


def save_cleaned(df):
    """Save the cleaned dataset to a CSV file."""
    os.makedirs("data/processed", exist_ok=True)

    df.to_csv(CLEAN_FILE, index=False)

    print(f"Cleaned data saved to {CLEAN_FILE}")


def load(df):
    """Load valid records into PostgreSQL."""
    print("Loading data into PostgreSQL...")

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            rows = [
                (
                    int(row.transaction_id),
                    row.customer_name,
                    row.restaurant,
                    row.category,
                    row.country,
                    int(row.quantity),
                    float(row.unit_price),
                    float(row.rating),
                    row.transaction_date,
                )
                for row in df.itertuples(index=False)
            ]

            cursor.executemany(
                """
                INSERT INTO restaurant_sales (
                    transaction_id,
                    customer_name,
                    restaurant,
                    category,
                    country,
                    quantity,
                    unit_price,
                    rating,
                    transaction_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING;
                """,
                rows,
            )

        connection.commit()
        print(f"Load completed. Records processed: {len(df)}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()