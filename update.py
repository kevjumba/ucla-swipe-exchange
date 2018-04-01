from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

table = dynamodb.Table('Swipes')

response = table.update_item(
    Key={
        'Location': "location"
    },
    UpdateExpression="set info.price = :prce, info.quantity=:amt, info.timee=:tme",
    ExpressionAttributeValues={
        ':prce': 6,
        ':amt': 20,
        ':tme': "5-6"
    },
    ReturnValues="UPDATED_NEW"
)

print("UpdateItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))