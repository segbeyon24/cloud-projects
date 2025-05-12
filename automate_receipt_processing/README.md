# AUTOMATED RECEIPT PROCESSING TOOL

- Goal
  - Automate Image to text storage and notification for receipts in a firm 


# Resources and Services
- AWS S3: Upload and store receipt files
- AWS Textract: Extract details of Uploaded files
- AWS DynamoDB: Save and organize important data
- AWS SES or SNS: Send summaries via email
- AWS Lambda: Automate the whole process

# Process

- S3 bucket receives a the image of a receipt (through direct uploading on the aws console or the endpoint of an application)
- An event notification is sent to a lambda function which triggers AWS Textract to transform the details of the image (receipt) to a json format, sends the data to a dynamoDB table and triggers the sns or ses to send the result to specific emails 



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
 


