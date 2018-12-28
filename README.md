# get_connect_ips
AWS Lambda to automate ip address range changes in firewalls. Produces a text file containing amazon ip ranges

## Description 
Amazon Web Services (AWS) publishes its current IP address ranges in JSON format at https://ip-ranges.amazonaws.com/ip-ranges.json This lambda utlizes the Python requests module to access Amazon's ip-ranges.json file, parse it for the IP addresses documented in the Amazon Connect Administrators Guide Network Ports and Protocols section of [Amazon Connect Troubleshooting and Best Practices](https://docs.aws.amazon.com/connect/latest/adminguide/troubleshooting.html#ccp-networking)

## How to configure this Lambda

The following variables are defined in lambda_function.py:

    bucket_name = "mybucketname"
    file_name = "amazon_connect_ips.txt"
    lambda_path = "/tmp/" + file_name
    s3_path = "connect/" + file_name
replace these with whatever you desire, however the lambda_path variable will always be `"/tmp/ " + file_name`

## How to deploy this Lambda

I began by defining this in the AWS console using the Lambda > Function Desginer to define the SNS trigger and the Lambda execution policy.

### Event Trigger
AmazonIpSpaceChanged SNS Topic: `arn:aws:sns:us-east-1:806199016981:AmazonIpSpaceChanged`

### Lambda Execution Policy
lambda-s3-role

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:*"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::*"
        }
    ]
}
```

To deploy this lambda, you will need to create a zip file containing the requests module dependency. This can be done using  `virtualenv`. See AWS instructions for [AWS Lambda Deployment Package in Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html#python-package-venv) for instructions on how to create and deploy the module. 

```
perseus:get_connect_ips jamesp$ virtualenv v-env
Using base prefix '/usr/local/Cellar/python/3.7.1/Frameworks/Python.framework/Versions/3.7'
New python executable in /Users/jamesp/Projects/get_connect_ips/v-env/bin/python3.7
Also creating executable in /Users/jamesp/Projects/get_connect_ips/v-env/bin/python
Installing setuptools, pip, wheel...
done.
perseus:get_connect_ips jamesp$ source v-env/bin/activate
(v-env) perseus:get_connect_ips jamesp$ pip install requests
Collecting requests
...

(v-env) perseus:get_connect_ips jamesp$ deactivate
perseus:get_connect_ips jamesp$ cd v-env/lib/python3.7/site-packages/
perseus:site-packages jamesp$ zip -r9 ~/Projects/get_connect_ips/get_connect_ips.zip .
...

perseus:get_connect_ips jamesp$ zip -g get_connect_ips.zip lambda_function.py 
  adding: lambda_function.py (deflated 57%)
  
perseus:get_connect_ips jamesp$ aws lambda update-function-code --function-name get_connect_ips --zip-file fileb://get_connect_ips.zip
```
