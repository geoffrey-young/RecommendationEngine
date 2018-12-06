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
#
# in order to get all 81,494 events loaded into DynamoDB using this
# script I adjusted DynamoDB from Provisioned to On Demand (see
# the Capacity tab in the AWS console), as the Provisioned defaults
# would not load all records in the 15 minute max Lambda runtime.
# using On Demand DynamoDB resources, this script loaded all events
# in 3 minutes (after one failure while DynamoDB scaled to the
# appropriate volume)

# python 2.7
import time
import json
import boto3

ATHENA_DATABASE = 'events'
ATHENA_TABLE = 'transformed_processed_events'
DYNAMODB_TABLE = 'events'
S3_OUTPUT = 's3://lambda-query-output'
S3_BUCKET = 'events_lambda_output'
PAGE_SIZE = 500

# number of athena read retries
RETRY_COUNT = 10

def lambda_handler(event, context):

    # you will want a different query, obviously
    query = "select * from {} order by event_id".format(ATHENA_TABLE)

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
    print("executing query {}".format(query_execution_id))

    for i in range(1, 1 + RETRY_COUNT):

        query_status = athena.get_query_execution(QueryExecutionId=query_execution_id)
        query_execution_status = query_status['QueryExecution']['Status']['State']

        if query_execution_status == 'SUCCEEDED':
            print("STATUS: {}".format(query_execution_status))
            break

        if query_execution_status == 'FAILED':
            raise Exception("STATUS: {}".format(query_execution_status))

        else:
            print("STATUS: {}... checking again in {} seconds".format(query_execution_status, i))
            time.sleep(i)
    else:
        athena.stop_query_execution(QueryExecutionId=query_execution_id)
        raise Exception('QUERY TIMED OUT')

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

        print("starting record set {}".format(count + 1))

        if not keys:
            keys = [c['VarCharValue'].encode('ascii','ignore') for c in result['ResultSet']['Rows'][0]['Data']]
            result['ResultSet']['Rows'].pop(0)

        with table.batch_writer(overwrite_by_pkeys=['event_id', 'event_id']) as batch:
            for row in result['ResultSet']['Rows']:
                values = [c.get('VarCharValue','').encode('ascii','ignore') for c in row['Data']]
                item = dict(zip(keys, values))
                filtered = dict((k,v) for k,v in item.iteritems() if v)
                batch.put_item(Item=filtered)
                count += 1

        print("finished writing {} total records".format(count))

    return count
