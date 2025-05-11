import boto3
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client('s3')
S3_BUCKET = os.getenv('S3_BUCKET', 'trade-logs-bucket')

def save_trade_to_s3(trade_data):
    date_prefix = datetime.utcnow().strftime('%Y/%m/%d')
    file_name = f"{date_prefix}/{trade_data['trade_id']}.json"
    s3.put_object(Bucket=S3_BUCKET, Key=file_name, Body=json.dumps(trade_data))
