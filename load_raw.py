import boto3
from botocore.exceptions import ClientError
import argparse
import os

#set up parser to add flag to run crawler
parser = argparse.ArgumentParser()
parser.add_argument("--run-crawler", action="store_true", help="Run the crawler after creating it")
args = parser.parse_args()

#globals
#AWS credentials in .env file in .gitignore for security reasons
glue = boto3.client('glue')
DB_NAME = 'pickleball_raw_db'
CRAWLER_NAME = 'pickleball_csv_crawler'
S3_PATH= os.getenv('S3_PATH', 's3://pickleball-data-bucket/')
CRAWLER_ROLE= os.getenv('CRAWLER_ROLE')

#create a new database
try: 
    glue.create_database(DatabaseInput={'Name': DB_NAME})
    print(f"{DB_NAME} was successfully created.")
except ClientError as e:
    if e.response['Error']['Code'] == 'AlreadyExistsException':
        print(f"{DB_NAME} already exists.")
    else:
        print(f"Error creating {DB_NAME}: {e}")

#Create Crawler to crawl s3 bucket and port into databse

try:
    glue.create_crawler(
        Name=CRAWLER_NAME,
        Role=CRAWLER_ROLE,
        DatabaseName=DB_NAME,
        Targets={'S3Targets': [{'Path': S3_PATH}]}
    )
    print('Glue Crawler successfully created')

    #check args to run crawler
    if args.run_crawler:
        glue.start_crawler(Name=CRAWLER_NAME)
        print(f"Running {CRAWLER_NAME}...")
    else:
        print("Skipping Crawler run.")
#if crawler already exists       
except ClientError as e:
    if e.response['Error']['Code'] == 'AlreadyExistsException':
        print(f"Crawler {CRAWLER_NAME} already exists.")
    else:
        print(f"Error creating crawler: {e}")
  

   
  

