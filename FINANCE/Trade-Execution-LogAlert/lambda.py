import json
import boto3
from collections import defaultdict
import time

sns = boto3.client('sns')
TOPIC_ARN = 'arn:aws:sns:us-east-1:<aws_account_id>:trade-alerts'

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        # Get the new trade
        obj = s3.get_object(Bucket=bucket, Key=key)
        trade = json.loads(obj['Body'].read())

        user_id = trade['user_id']
        timestamp = trade['timestamp']

        # (In real case, we'd check trade history; here we just alert on big trades)
        if int(trade['qty']) > 10000:
            message = f"High volume trade detected from user {user_id}: {trade}"
            sns.publish(TopicArn=TOPIC_ARN, Message=message, Subject="ALERT: Unusual Trade Volume")
