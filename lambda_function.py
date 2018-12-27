import json
import requests
import boto3

bucket_name = "stellaartois"
file_name = "amazon_connect_ips.txt"
lambda_path = "/tmp/" + file_name
s3_path = "connect/" + file_name

def lambda_handler(event, context):
    # TODO implement
    ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()['prefixes']
    connect_ranges = [] #get ready to build a big list

    #Amazon Connect needs access to AMAZON_CONNECT, EC2, and CLOUDFRONT over port 443
    connect_ips = [item['ip_prefix'] for item in ip_ranges if (item["service"] == "AMAZON_CONNECT") and (item["region"] == "us-east-1")]
    for ip in connect_ips:
        connect_ranges.append(ip)

    ec2_ips = [item['ip_prefix'] for item in ip_ranges if (item["service"] == "EC2") and (item["region"] == "us-east-1")]
    for ip in ec2_ips:
        connect_ranges.append(ip)

    cloudfront_ips = [item['ip_prefix'] for item in ip_ranges if (item["service"] == "CLOUDFRONT") and (item["region"] == "us-east-1")]
    for ip in cloudfront_ips:
        connect_ranges.append(ip)

    #write out a temp file until I figure out how to stream this directly to S3
    f = open(lambda_path, 'w+')
    for ip in connect_ranges:
        f.write("%s\n" % ip)
    f.close()

    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(lambda_path, bucket_name, s3_path)
    return {
        'statusCode': 200,
        'body': json.dumps('success')
    }
#delete these
#event = "foo"
#context = "bar"
#lambda_handler(event, context) #I'm just here for debugging
