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
  
aws lambda update-function-code --function-name get_connect_ips --zip-file fileb://get_connect_ips.zip
{
    "TracingConfig": {
        "Mode": "PassThrough"
    }, 
    "CodeSha256": "dxAYqQNP6+rlbX0n4GB2/aPRkHqBr0+TMcGijyWBQMk=", 
    "FunctionName": "get_connect_ips", 
    "CodeSize": 4558403, 
    "RevisionId": "efb9ef79-83fe-4f73-84cc-9d843362eca0", 
    "MemorySize": 128, 
    "FunctionArn": "arn:aws:lambda:us-east-1:*:function:get_connect_ips", 
    "Version": "$LATEST", 
    "Role": "arn:aws:iam::*:role/lambda-s3-role", 
    "Timeout": 3, 
    "LastModified": "2018-12-24T20:21:39.002+0000", 
    "Handler": "lambda_function.lambda_handler", 
    "Runtime": "python3.7", 
    "Description": ""
}
```
