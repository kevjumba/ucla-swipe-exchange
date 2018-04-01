from __future__ import print_function # Python 2/3 compatibility
import boto3
from botocore.exceptions import ClientError
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
def eraseItem(m_key):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    
    table = dynamodb.Table('Swipes')
    
    
    print("Attempting a conditional delete...")
    
    try:
        response = table.delete_item(
            Key={
                'Location': m_key
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        print("DeleteItem succeeded:")

