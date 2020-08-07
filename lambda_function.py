# James Bower / @jamesbower

import boto3
import botocore.vendored.requests.packages.urllib3 as urllib3
import json
import logging

log = logging.getLogger()
log.setLevel(logging.INFO)
s3 = boto3.client('s3')
url1 = "https://api.github.com/repos/frida/frida/releases/latest"
url2 = "https://github.com/frida/frida/releases/download/"
bucket = "S3-Bucket"

def lambda_handler(event, context):
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    response = http.request('GET', url1, preload_content=False, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    data = json.loads(response.data.decode('utf-8'))
    tag = data['tag_name']
    location = url2 + tag + "/frida-server-" + tag + "-android-arm.xz"
    filename = ("frida-server-" + tag + "-android-arm.xz")
    request = http.request('GET', location, preload_content=False, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    fileobj = request
    path = f"s3://{bucket}/{filename}"
#    log.info(f"Uploading file to {path}")
    s3.upload_fileobj(fileobj, bucket, filename)
    return {
        "statusCode": 200,
        "body": json.dumps('Upload Successful')
    }
