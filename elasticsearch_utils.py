import requests
from datetime import datetime

elasticsearch_url = 'http://localhost:9200/'
elasticsearch_type = 'bill'

def getRecordsWrongBillNumber():
	elasticsearch_query = '{"query":{"bool":{"must":{"match":{"_type":"' + elasticsearch_type + '"}},"filter":{"regexp":{"details.number":{"value":"[0-9]{8}"}}}}}}'
	elasticsearch_query_response = requests.get(elasticsearch_url + '_search', data = elasticsearch_query)

	if elasticsearch_query_response.status_code != 200:
		print(str(elasticsearch_query_response.status_code) + ' ' + elasticsearch_query_response.text)
		return None
	else:
		return elasticsearch_query_response.json()


def updateRecordWrongBillNumber(elasticSearchRecord):
	elasticsearch_url_update = elasticSearchRecord.index + '/' + elasticsearch_type + '/' + elasticSearchRecord.id
	elasticsearch_data_update = '{"doc":{"details":{"number":"' + elasticSearchRecord.number[:7] + '"}}}'
	elasticsearch_update_response = requests.post(elasticsearch_url + elasticsearch_url_update + '/_update', data = elasticsearch_data_update)

	if elasticsearch_update_response.status_code == 200:
		print(str(datetime.now()) + ' Update ' + elasticSearchRecord.index + ' ' + elasticSearchRecord.id + ' with number: ' + elasticSearchRecord.number[:7])
	else:
		print(str(datetime.now()) + ' Error ' + elasticSearchRecord.index + ' ' + elasticSearchRecord.id + ' with number: ' + elasticSearchRecord.number[:7] +
			  ' code: ' + str(elasticsearch_update_response.status_code) + ' description: ' + elasticsearch_update_response.text)
