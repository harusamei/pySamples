from elasticsearch import Elasticsearch
from esIndex import test_field_analyzer


class ESQuery:

    def __init__(self, host='localhost', port='9200'):
        self.host = host
        self.port = port
        self.es = Elasticsearch(hosts=[{'host': self.host, 'port': self.port,'scheme': 'http'}])
        if not self.es.ping():
            raise ValueError("Connection failed")
        else:
            print("Connected to Elasticsearch")


""" 

#field-query = {product_name: "小新"}   
def query_word(index, fq):
    query = {
        "size": 3,  # Return top3 results
        "query": {
            "match": fq
        }
    }
    # Execute the query
    return es.search(index=index, body=query)

#可使用"fields": ["*"], 表示所有字段
def query_multi_fields(index,word,fieldList):
    query = {
        "size": 3,
        "query": {
            "multi_match": {
                "query": word,
                "fields": fieldList
            }
        }
    }
    return es.search(index=index, body=query)

def query_either_should_must(index, fqList, opt="should"):
    if opt != "should":
        opt = "must"
    
    query = {
        "size": 3,
        "query": {
            "bool": {
                opt: [{"match": fq} for fq in fqList]
            }
        }
    }
    return es.search(index=index, body=query)

# 返回满足所有must和至少一个should的文档
def query_both_should_must(index, must_list, should_list):
    query = {
        "query": {
            "bool": {
                "must": [{"match": fq} for fq in must_list],
                "should": [{"match": fq} for fq in should_list],
                "minimum_should_match": 1
            }
        }
    }
    return es.search(index=index, body=query)

# 基于field的聚合
def aggregate(index, field):
    query = {
        "size": 0,
        "aggs": {
            "properties": {
                "terms": {
                    "field": field
                }
            }
        }
    }
    response = es.search(index=index, body=query)
    return response['aggregations']['properties']['buckets']

#满足某查询条件下的基于field的聚合
def query_agg(index, fqlist, field):
    query = {
        "query": {
            "bool": {
                "should": [{"match": fq} for fq in fqlist]
            }
        },
        "size": 0,
        "aggs": {
            "properties": { #聚合依据
                    "terms": {
                        "field": field,
                        "size": 10
                    }
            }
        }
    }
    response = es.search(index=index, body=query)
    return response['aggregations']['properties']['buckets']
# 数值统计
def query_range(index, field, upper, lower):
    query = {
        "size": 3,
        "query": {
            "range": {
                field: {
                    "gte": lower, #大于等于low
                    "lte": upper
                }
            }
        }
    }
    return es.search(index=index, body=query)

def query_average(index, field):
    query = {
        "size": 0,
        "aggs": {
            "average": {
                "avg": {
                    "field": field
                }
            }
        }
    }

    response = es.search(index=index, body=query)
    avg_value = response['aggregations']['average']['value']
    return avg_value

#返回最大或最小值
def query_max_min(index, field, most):
    if most == "max":
        m_value="max_value"
    else:
        m_value="min_value"
        most = "min"   
    query = {
        "size": 0,
        "aggs": {
            m_value: {
                most: {
                    "field": field
                }
            }
        }
    }

    response = es.search(index=index, body=query)
    return response['aggregations'][m_value]['value']

def list_result(response):
    #满足查询条件的文档数
    print("Got %d Hits:" % response['hits']['total']['value'])
    for hit in response['hits']['hits']:
        print(hit["_source"]) 

def field_result(response, field):
    for hit in response['hits']['hits']:
        print(hit["_source"].get(field))

#用户的问题是“请问是否有叫小新的产品”， 请根据下面的查询结果回复用户的问题
def generate_answer(query,response):
    print("about %s, Got %d Hits:" % (query,response['hits']['total']['value']))
    print(response)

 """
def main():
    # Call the query_es_index function
    es = ESQuery('10.110.153.75', 9200)
    # index="leproducts"
    # result = query_word(index, {"product_name": "小新"})
    # list_result(result)

if __name__ == '__main__':
    main()