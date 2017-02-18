# Need to install requests package for python "pip install requests"

import sys
import entities, elasticsearch_utils

print('Getting bills from Elasticsearch to fix')

elasticsearch_response = elasticsearch_utils.getRecordsWrongBillNumber()

if elasticsearch_response is None:
	sys.exit(-1)

print('Gathering information from Elasticsearch response')

elastic_search_records = []

for hit in elasticsearch_response['hits']['hits']:
	elastic_search_records.append(entities.ElasticSearchRecord(hit['_index'], hit['_id'], hit['_source']['details']['number']))

print('Updating ' + str(len(elastic_search_records)) + ' records in Elasticsearch')

for record in elastic_search_records:
	elasticsearch_utils.updateRecordWrongBillNumber(record)

print('Fix finished')
sys.exit(0)
