import boto3
import json
import gzip
import os

s3 = boto3.client('s3')
sns = boto3.client('sns')

SNS_TOPIC_ARN = 'arn:aws:sns:<REGION>:<ACCOUNT_ID>:TicTacToeLogTopic'

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        response = s3.get_object(Bucket=bucket, Key=key)
        raw_log = response['Body'].read().decode('utf-8')
        
        # Clean up log into JSON-like entries
        log_lines = raw_log.strip().splitlines()
        events = [{"event": line} for line in log_lines if line.strip()]
        
        message = json.dumps({"log_events": events}, indent=2)
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Tic Tac Toe Game Log",
            Message=message
        )
        
        return {
            'statusCode': 200,
            'body': 'SNS Notification sent.'
        }