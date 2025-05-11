# AUTOMATED RECEIPT PROCESSING TOOL

- Goal
  - Automate Image to text storage and notification for receipts in a firm 


# Resources and Services
- AWS S3: Upload and store receipt files
- AWS Textract: Extract details of Uploaded files
- AWS DynamoDB: Save and organize important data
- AWS SES: Send summaries via email
- AWS Lambda: Automate the whole process

# Process
- Clone and run the application

- Create S3 bucket to store the log file
  - the app generates logs and stores them in `tic_tac_toe.log` file - this file is created, if not already existing in the app's directory, everytime the game begins
  - a cronjob runs the file `upload-log.sh` every minute, if a game has started (perhaps modify post per event).
  - the `upload-log.sh` file sends the log file to the s3 bucket


- Lambda Function: 
  - reads the file from S3
  - converts the content into JSON format
  - sends it to an SNS topic.


- S3 Bucket Notification
  - notifies the Lambda function when a new log file is uploaded.


- SNS Topic: 
  - subscribers receive emails when the Lambda publishes a message.

  - NB: the `process_log.sh` file should accomplish this task without the need for AWS s3, lambda and SNS cloud services, if SMTP is installed on the linux machine.

# Breaking it down

1. Create S3 Bucket
   - create S3 bucket <receiptBucket>
   - creeate a folder in the bucket <incoming>

2. Create Dynamodb table
   - create table <receipts>
     - add name
     - partition key (receipt_id and date, both as string datatypes)

3. Create SES
   - create identity
    - select email and add your email
    - go to email to confirm the "subscription"

4. Create IAM role
   - create role
     - select AWS service
     - select lambda as the "Use case"
     - permissions:
       - select AmazonS3ReadOnlyAccess
       - select AmazonTextractFullAccess
       - select AmazonDynamoDBFullAccess
       - select AmazonSESFullAccess
       - select AWSLambda_Access

5. Create Lambda function
   - select python 3.9
   - select "Use existing role" as Execution role
     - select th role created in (4) above
   - Go to Configurations and change the "Timeout" from 3 seconds to 3 minutes
   - Add the environment variables in the function's code
   - paste the lambda.py code in the ide and deploy the code


6. Setup S3 event Notification
   - navigate to the S3 bucket created in (1) earlier
   - go to "Properties" an click on "create event notification"
     - fill the form, including checking the "All object create events"
     - scroll down and select lambda function as the "Destination" and select the lambda creaated in (5)


7. Upload a receipt image to your S3 bucket (in console or from an app) and you should receive a text break-down of the content of the receipt uploaded in your email
   - Check the lambda monitor feature and/or the DynamoDB table created to verify/track the process.
   


# Possible Issues
 


