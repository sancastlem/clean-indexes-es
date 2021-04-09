## Imports
import boto3
import os
import curator

from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

## Global
endpoint = os.environ['endpoint'] # Provide the elasticsearch endpoint
region = os.environ['region'] # Provide the region
days = int(os.environ['days']) # Number of days to maintenance
regex = os.environ['regex'] # Kind type for regex filter
exclude = os.environ['exclude'] # Exclude index that you don't want to delete

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Lambda execution starts here.
def main(event, context):

    # Build the Elasticsearch clientself
    es = Elasticsearch (
        hosts=[{'host': endpoint, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    
    # Create the index list and filter, excluding .kibana index
    index_list = curator.IndexList(es)
    index_list.filter_kibana(exclude=True)

    # Optionally, if field filter is not empty, then also exclude the indexes inserted it
    if exclude != "" and regex != "":
        index_list.filter_by_regex(kind=regex, value=exclude, exclude=True)
        index_list.filter_by_age(source='creation_date', direction='older', unit='days', unit_count=days)
    else:
        index_list.filter_by_age(source='creation_date', direction='older', unit='days', unit_count=days)


    # Delete indexes
    print("Found %s indexes to delete" % len(index_list.indices))
    
    if len(index_list.indices) > 0:
        print('Indexes found: {0}'.format(index_list.indices))
        curator.DeleteIndices(index_list).do_action()

        print('Indices deleted successfully.')
        
    else:
        print('No indexes to delete.')