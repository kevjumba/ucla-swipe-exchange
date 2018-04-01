from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

def insert(m_key, m_price , m_quantity, m_timee , m_location):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('Swipes') # table 
    
    
    #updates totalNumber of items
    response = table.update_item(
        Key={
            'Location': "totalCount",
        },
        UpdateExpression="set totalNum = totalNum + :val",
        ExpressionAttributeValues={
            ':val': 1
        },
        ReturnValues="UPDATED_NEW"
    )
    
    numItems = 0
    #get the current count of items
    response = table.query(
        KeyConditionExpression=Key('Location').eq('totalCount') 
    )
    
    for i in response['Items']:
        numItems = (i['totalNum'])
    
    convertedNumItems = str(numItems)   
    
    #inserting the new item with the new items
    response = table.put_item(
       Item={
            'Location': m_location + convertedNumItems,
            'info': {
                'price': m_price,
                'quantity': m_quantity,
                'timee': m_timee
            }
        }
    )
    
    
    
    print("PutItem succeeded:")
    #print(json.dumps(response, indent=4, cls=DecimalEncoder)) 



def main():
    insert("Bplato",5,1,"3-9","Bplato")

main()