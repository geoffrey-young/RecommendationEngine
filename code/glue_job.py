# this is a glue job that reads input events from csv files on s3
# and outputs them in parquet format to s3.  it is mostly code generated
# using the aws console, with the addition of a self-coded filter to serve
# as an example of extending jobs.

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

## @type: DataSource
## @args: [database = "events", table_name = "events_input", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "events", table_name = "events_input", transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("event_description", "string", "event_description", "string"), ("event_end_utc", "string", "event_end_utc", "string"), ("event_id", "string", "event_id", "string"), ("event_name", "string", "event_name", "string"), ("event_start_utc", "string", "event_start_utc", "string"), ("facebook_event_id", "string", "facebook_event_id", "string"), ("hashtag", "string", "hashtag", "string"), ("organization_id", "string", "organization_id", "string"), ("organization_name", "string", "organization_name", "string"), ("tags", "array", "tags", "array"), ("venue_city", "string", "venue_city", "string"), ("venue_name", "string", "venue_name", "string"), ("venue_state", "string", "venue_state", "string"), ("venue_street", "string", "venue_street", "string"), ("venue_timezone", "string", "venue_timezone", "string"), ("venue_zip", "string", "venue_zip", "string")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("event_description", "string", "event_description", "string"), ("event_end_utc", "string", "event_end_utc", "string"), ("event_id", "string", "event_id", "string"), ("event_name", "string", "event_name", "string"), ("event_start_utc", "string", "event_start_utc", "string"), ("facebook_event_id", "string", "facebook_event_id", "string"), ("hashtag", "string", "hashtag", "string"), ("organization_id", "string", "organization_id", "string"), ("organization_name", "string", "organization_name", "string"), ("tags", "array", "tags", "array"), ("venue_city", "string", "venue_city", "string"), ("venue_name", "string", "venue_name", "string"), ("venue_state", "string", "venue_state", "string"), ("venue_street", "string", "venue_street", "string"), ("venue_timezone", "string", "venue_timezone", "string"), ("venue_zip", "string", "venue_zip", "string")], transformation_ctx = "applymapping1")

## @type: DropNullFields
## @args: [transformation_ctx = "dropnulls2"]
## @return: dropnulls2
## @inputs: [frame = applymapping1]
dropnulls2 = DropNullFields.apply(frame = applymapping1, transformation_ctx = "dropnulls2")

## @type: Filter
## @args: [f = filter_function, transformation_ctx = "filter3"]
## @return: filter3
## @inputs: [frame = dropnulls2]
def filter_function(dynamicRecord):
	if "PA" in dynamicRecord["venue_state"]:
		return True
	else:
		return False
filter3 = Filter.apply(frame = dropnulls2, f = filter_function, transformation_ctx = "filter3")

## @type: DataSink
## @args: [connection_type = "s3", connection_options = {"path": "s3://cis562/output/processed_events"}, format = "json", transformation_ctx = "datasink3"]
## @return: datasink4
## @inputs: [frame = filter3]
datasink4 = glueContext.write_dynamic_frame.from_options(frame = filter3, connection_type = "s3", connection_options = {"path": "s3://cis562/output/processed_events"}, format = "parquet", transformation_ctx = "datasink4")

job.commit()
