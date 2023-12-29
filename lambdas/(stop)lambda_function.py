import boto3
import json
import os

region = 'ca-central-1'
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    envInstID = os.environ.get('INSTANCE_ID')
    ec2.stop_instances(InstanceIds=[envInstID])

    return {
        'statusCode': 200,
        'body': json.dumps('Stoping Instance {instID}'.format(instID=envInstID))
    }