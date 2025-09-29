import boto3
import argparse

#set up parser to add dataset

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Path to local csv file")
args = parser.parse_args()

print(f"Uploading {args.filename}...")

s3 = boto3.client('s3', region_name='us-west-2')
BUCKET_NAME = 'pickleball-data-bucket'
s3.upload_file(args.filename, BUCKET_NAME, 'data.csv' )

print(f"Successfully uploaded {args.filename} to s3://{BUCKET_NAME}/data.csv")
  