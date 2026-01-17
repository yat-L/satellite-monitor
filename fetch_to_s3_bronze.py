import os
import time
from datetime import datetime

import boto3
import requests
from botocore.exceptions import ClientError

# --- CONFIGURATION ---
# Best Practice: Load these from Environment Variables in production
DSN_XML_URL = "https://eyes.nasa.gov/dsn/data/dsn.xml"
AWS_REGION = "us-east-1"
S3_BUCKET_NAME = "nasa-analytics-lakehouse"
S3_RAW_PREFIX = "bronze/dsn_telemetry/v1"  # Partition path


def fetch_dsn_data():
    """
    Extracts raw XML data from the NASA DSN feed.
    Returns: Bytes content of the XML or None if failed.
    """
    print(f"[{datetime.now()}] Connecting to NASA DSN Stream...")
    try:
        # User-Agent headers often help prevent 403 Forbidden errors
        headers = {"User-Agent": "NASA-Data-Pipeline/1.0", "Accept": "application/xml"}
        response = requests.get(DSN_XML_URL, headers=headers, timeout=10)
        response.raise_for_status()
        print(
            f"[{datetime.now()}] Data fetched successfully. Size: {len(response.content)} bytes."
        )
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"!! Network Error fetching data: {e}")
        return None


def upload_to_s3(content, bucket_name, prefix):
    """
    Uploads the raw content to AWS S3 with a Hive-style partition structure.
    Naming Convention: YYYY/MM/DD/dsn_raw_HHMMSS.xml
    """
    s3_client = boto3.client("s3", region_name=AWS_REGION)

    # Generate Partition Keys (Hive Style)
    now = datetime.utcnow()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    timestamp_id = now.strftime("%H%M%S")

    # Construct Object Key (File Path)
    # e.g., bronze/dsn_telemetry/v1/year=2024/month=01/day=15/dsn_20240115_143000.xml
    object_key = (
        f"{prefix}/year={year}/month={month}/day={day}/"
        f"dsn_{now.strftime('%Y%m%d_%H%M%S')}.xml"
    )

    try:
        print(f"[{datetime.now()}] Uploading to s3://{bucket_name}/{object_key} ...")

        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=content,
            ContentType="application/xml",
            Metadata={"source": "nasa_dsn_feed", "ingest_timestamp": str(time.time())},
        )
        print(f"[{datetime.now()}] Upload Successful.")
        return True

    except ClientError as e:
        print(f"!! AWS Client Error: {e}")
        return False


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. EXTRACT
    raw_xml_data = fetch_dsn_data()

    # 2. LOAD (to Data Lake)
    if raw_xml_data:
        success = upload_to_s3(raw_xml_data, S3_BUCKET_NAME, S3_RAW_PREFIX)

        if success:
            print(">>> Pipeline Step 1 (Extract -> Raw Store) Complete.")
        else:
            print(">>> Pipeline Failed during S3 Upload.")
            exit(1)
    else:
        print(">>> Pipeline Failed during Extraction.")
        exit(1)
