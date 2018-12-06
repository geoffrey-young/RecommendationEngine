# this is an AWS Lambda function that will query DynamoDB and return
# a single event.  it is designed to be called by an API Gateway
# resource in the following format:
#
#  GET /event/{id}
#
# see
#
#   img/api_gateway.png
#
# for an example setup.

# python 2.7
import json
import boto3

DYNAMODB_TABLE = 'events'

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE)

    try:
        event_id = event['pathParameters']['id']

        print("event_id: {}".format(event_id))

        response = table.get_item(Key={
            'event_id':event_id
        })

        return {
            "statusCode": 200, 
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response['Item'])
        }

    except:
        return {
            "statusCode": 404
        }
