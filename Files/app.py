import os
import boto3
import pandas as pd
from sqlalchemy import create_engine
from botocore.exceptions import ClientError

# ENV VARIABLES
S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("S3_KEY")

RDS_HOST = os.getenv("RDS_HOST")
RDS_USER = os.getenv("RDS_USER")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_DB = os.getenv("RDS_DB")
RDS_TABLE = os.getenv("RDS_TABLE")

GLUE_DB = os.getenv("GLUE_DB")
GLUE_TABLE = os.getenv("GLUE_TABLE")
GLUE_S3_PATH = os.getenv("GLUE_S3_PATH")


def read_from_s3():
    print("📥 Reading data from S3...")
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
    df = pd.read_csv(obj["Body"])
    return df


def upload_to_rds(df):
    print("📤 Uploading data to RDS...")
    try:
        engine = create_engine(
            f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}/{RDS_DB}"
        )
        df.to_sql(RDS_TABLE, con=engine, if_exists="replace", index=False)
        print("✅ Data inserted into RDS")
    except Exception as e:
        print(f"❌ RDS Failed: {e}")
        raise


def fallback_to_glue():
    print("⚠️ Falling back to AWS Glue...")
    glue = boto3.client("glue")

    try:
        glue.create_table(
            DatabaseName=GLUE_DB,
            TableInput={
                "Name": GLUE_TABLE,
                "StorageDescriptor": {
                    "Columns": [
                        {"Name": "id", "Type": "int"},
                        {"Name": "name", "Type": "string"},
                        {"Name": "age", "Type": "int"},
                    ],
                    "Location": GLUE_S3_PATH,
                    "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                    "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "SerdeInfo": {
                        "SerializationLibrary": "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
                        "Parameters": {"field.delim": ","},
                    },
                },
                "TableType": "EXTERNAL_TABLE",
            },
        )
        print("✅ Glue Table Created")
    except ClientError as e:
        print(f"❌ Glue Failed: {e}")


def main():
    try:
        df = read_from_s3()
        upload_to_rds(df)
    except Exception:
        fallback_to_glue()


if __name__ == "__main__":
    main()
