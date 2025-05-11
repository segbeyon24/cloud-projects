# Trade Execution Logger and Anomaly Alerting

- Goal
  - Flask-based Trade Execution Logger with real-time alerting using AWS services. This project simulates a real-world backend that receives trade orders, stores them, and raises alerts on suspicious activity.


# Resources and Services
- Flask: API server to receive trade data.
- EC2: Linux machine to host the application
- AWS S3: Stores logs (optionally DynamoDB or RDS for live systems).
- AWS Lambda: Monitors S3 for new logs, analyzes them for anomalies.
- AWS SNS: Sends email/SMS alerts to subscribers.



# Process
- Clone and run the application
```bash
git clone <repo>
cd FINANCE/Trade-Execution-LogAlert/trade-logger
pip install -r requirements.txt
python app.py
```

- create a .env file and add your AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and the name of your S3_BUCKET

- Sample form to submit from terminal
```bash
curl -X POST http://localhost:5000/trade \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u123", "symbol": "AAPL", "qty": 15000, "price": 172.5, "type": "buy"}'
```


- Lambda Function: 
  - reads the file from S3
  - converts the content into JSON format
  - sends it to an SNS topic.


- S3 Bucket Notification
  - notifies the Lambda function when a new log file is uploaded.


- SNS Topic: 
  - subscribers receive emails when the Lambda publishes a message.


# Breaking it down

1. Create S3 Bucket
   - create S3 bucket <trade-alert>

<!-- 2. Create Dynamodb table
   - create table <receipts>
     - add name
     - partition key (receipt_id and date, both as string datatypes) -->

3. Create SNS topic and subscription

4. Create IAM role
   - create role
     - select AWS service
     - select lambda as the "Use case"
     - permissions:
       - select AmazonS3ReadOnlyAccess
       - select AmazonSNSFullAccess
       - select AWSLambda_Access

5. Create Lambda function
   - select python 3.9
   - select "Use existing role" as Execution role
     - select th role created in (4) above
   - Add the environment variables in the function's code
   - paste the lambda.py code in the ide and deploy the code


6. Setup S3 event Notification
   - navigate to the S3 bucket created in (1) earlier
   - go to "Properties" an click on "create event notification"
     - fill the form, including checking the "All object create events"
     - scroll down and select lambda function as the "Destination" and select the lambda creaated in (5)


7. Upload a receipt image to your S3 bucket (in console or from an app) and you should receive a text break-down of the content of the receipt uploaded in your email
   - Check the lambda monitor feature and/or the DynamoDB table created to verify/track the process.

8. Mail is only sent if there is an anomaly detected - in this case, it is for trades beyond 10,000 unit volume of stocks
   


# Possible Issues

- The frontend still needs the form submission format to be changes to application/json
- follow the instructions to avoid "errors due to parallax"