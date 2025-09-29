# AWS Data Pipeline Project – Pickleball Analytics

Hi, thanks for viewing this project!

This is a portfolio project where I practiced AWS pipeline development using a pickleball games dataset.  
The goal was to build a modern data pipeline that ingests raw data, transforms it, and makes it available for analytics. 

---

## Pipeline Overview

This AWS data pipeline:
1. Ingests raw CSV files into Amazon S3
2. Catalogs them with AWS Glue Crawler
3. Transforms data using PySpark in a Glue ETL Job
4. Loads the processed data into Snowflake for analytics

---

## Architecture Diagram

![Architecture Diagram](images/workflow.png)

---

## Tech Stack

- AWS S3 – Raw & processed data storage  
- AWS Glue – Data Catalog + PySpark ETL  
- Python – boto3, argparse for automation  
- Snowflake – Cloud data warehouse for analytics  

---

## Screenshots
### S3 Upload Through Python boto3
![S3 Upload through Python boto3](screenshots/boto3_upload.png)
![bucket](screenshots/aws_bucket_with_csv_upload.png)

### PySpark ETL Job Script
```py
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

#Added arguments to remove hardcoded values
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'DB_NAME', 'TABLE_NAME', 'OUTPUT_PATH'])
  
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

#use provided args
job.init(args['JOB_NAME'], args)

#added args to dynamic frame creation
dyf = glueContext.create_dynamic_frame.from_catalog(database=args['DB_NAME'], table_name=args['TABLE_NAME'])

df = dyf.toDF()

#Map Pro and Senior Pro skill_lvl values to DUPR scores
print('Starting Transformation...')
from pyspark.sql import functions as F

df = df.withColumn(
    'skill_lvl_clean',
    F.when(F.col('skill_lvl') == 'Pro', '6.0')\
    .when(F.col('skill_lvl') == 'Senior Pro', '5.0')\
    .otherwise(F.col('skill_lvl'))
)

#convert DUPR scores to float
df = df.withColumn('skill_lvl_clean', F.col('skill_lvl_clean').cast('float'))

#Designate Winner column
df = df.withColumn('winner', F.col('w_team_id'))

#make dt_played into datetime
df = df.withColumn('dt_played', F.to_date('dt_played', 'yyyy-MM-dd'))

#add a score difference aggregate column
df = df.withColumn('score_diff', F.col('score_w') - F.col('score_l'))

#write to a new csv and put in processed s3 bucket folder
#added output path arg to write method
print('Writing results to s3...')
df.write.mode('overwrite').csv(args['OUTPUT_PATH'])

print('Job complete.')
job.commit()
```
![PySpark ETL Job Script](screenshots/PySparkETL.png)

### Running ETL job with Parameters
![Running ETL job with Parameters](screenshots/Run_job_parameters.png)

---

## Results

Here’s an example analytics query in Snowflake:

```sql
SELECT skill_lvl, COUNT(*) AS games_played
FROM pickleball_games
GROUP BY skill_lvl
ORDER BY games_played DESC;
```
