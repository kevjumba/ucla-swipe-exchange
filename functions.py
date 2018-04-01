from __future__ import print_function # Python 2/3 compatibility
import boto3
from botocore.exceptions import ClientError
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr


def create_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    
    
    table = dynamodb.create_table(
        TableName='Swipes',
        KeySchema=[
            {
                'AttributeName': 'Location',
                'KeyType': 'HASH'  #Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Location',
                'AttributeType': 'S'
            },
    
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    
    print("Table status:", table.table_status)
    return




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
    
    return    
        
        
def insertOrUpdate(m_key, m_price , m_quantity, m_early, m_late):
    
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
            'Location': m_key + convertedNumItems,
            'info': {
                'price': m_price,
                'quantity': m_quantity,
                'early': m_early,
                'late': m_late
            }
        }
    )
    
    print("PutItem succeeded:")
    return



def getItem(m_key):
    dynamodb = boto3.resource("dynamodb", region_name='us-west-1')
    
    table = dynamodb.Table('Swipes')
    
    try:
        response = table.get_item(
            Key={
                'Location': m_key
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("GetItem succeeded:")
    return item #returns json Item



def queryByKey(m_key):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    
    table = dynamodb.Table('Swipes')
    
    list = []
    
    
    response = table.query(
    )
    
    for i in response['Items']:
        check = i['Location']
        if not check.find(m_key):
            list.append(check)
    return list   
        
        
def queryByAttributes(m_key, m_price, m_timee, m_quantity):#query by attributes
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    
    table = dynamodb.Table('Swipes')
    
    list = []
    
    
    response = table.scan(
    FilterExpression= Attr('info.early').lte(m_timee) & Attr('info.late').gte(m_timee)  & Attr('info.price').lte(m_price) & Attr('info.quantity').eq(m_quantity)
    )
    
    for i in response['Items']:
        check = i['Location']
        if not check.find(m_key):
            list.append(check)
    return list  


def scan(m_key):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    
    table = dynamodb.Table('Swipes')
    
    list = [] 
    
    response = table.scan(

        )
    
    for i in response['Items']:
        check = i['Location']
        if not check.find(m_key):
            list.append(check)
    return list






#MAIN
def main():
    insertOrUpdate("Bplato", 8 , 4, 3, 6 )
    #eraseItem("Bplato11")
    #getItem("Bplato12")
    #print(queryByKey("B"))
    #print(scan("Bplato"))
    #insertOrUpdate("Bplato", 20 , 20, 3, 4)
    #print(queryByAttributes("Bplato",20,3,20))

main()
