# this is an AWS Lambda function that will query Athena and insert
# the query results into DynamoDB.  it borrows from the following gists:
#
#   https://gist.github.com/y4e/03d5d783ac160fc0f657d5ef038a562f
#   https://gist.github.com/schledererj/b2e2a800998d61af2bbdd1cd50e08b76
#
# you will likely need to add IAM policies to your Lambda function that
# allow full access of S3, DynamoDB, and Athena for this to work. see
#
#   img/lambda_iam_policies.png
# 
# for an example.

from pprint import pprint
import time
import json
import boto3

ATHENA_DATABASE = 'events'
ATHENA_TABLE = 'transformed_processed_events'
DYNAMODB_TABLE = 'events'
S3_OUTPUT = 's3://lambda-query-output'
S3_BUCKET = 'events_lambda_output'

# boto3 can handle page sizes up to 1000, both for reads from Athena
# as well as writes to DynamoDB.  so bump this up for large data movements.
PAGE_SIZE = 5

# number of athena read retries
RETRY_COUNT = 10

def lambda_handler(event, context):

    # you will want a different query, obviously
    query = "select event_id, venue_city, venue_state, event_name from {} where event_name like '%wine%' order by event_id limit 20".format(ATHENA_TABLE)

    athena = boto3.client('athena')

    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': ATHENA_DATABASE
        },
        ResultConfiguration={
            'OutputLocation': S3_OUTPUT,
        }
    )

    query_execution_id = response['QueryExecutionId']
    print(query_execution_id)

    for i in range(1, 1 + RETRY_COUNT):

        query_status = athena.get_query_execution(QueryExecutionId=query_execution_id)
        query_execution_status = query_status['QueryExecution']['Status']['State']

        if query_execution_status == 'SUCCEEDED':
            print("STATUS:" + query_execution_status)
            break

        if query_execution_status == 'FAILED':
            raise Exception("STATUS:" + query_execution_status)

        else:
            print("STATUS:" + query_execution_status)
            time.sleep(i)
    else:
        athena.stop_query_execution(QueryExecutionId=query_execution_id)
        raise Exception('TIME OVER')
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE)
    keys = None
    count = 0
        
    results_paginator = athena.get_paginator('get_query_results')
    results_iterator = results_paginator.paginate(
        QueryExecutionId=query_execution_id,
            PaginationConfig={
            'PageSize': PAGE_SIZE,
            'StartingToken': None
        }
    )
    
    for result in results_iterator:
        
        if not keys:
            keys = [c['VarCharValue'].encode('ascii','ignore') for c in result['ResultSet']['Rows'][0]['Data']]
            result['ResultSet']['Rows'].pop(0)
        
        with table.batch_writer(overwrite_by_pkeys=['event_id', 'event_id']) as batch:
            for row in result['ResultSet']['Rows']:
                values = [c['VarCharValue'].encode('ascii','ignore') for c in row['Data']]
                item = dict(zip(keys, values))
                batch.put_item(Item=item)
                #pprint("added {}".format(json.dumps(item)))
                count += 1
        
    return count
