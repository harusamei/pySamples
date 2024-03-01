from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import sys

def create_index(es, index_name, body=None, analyzer=None):

    if es.indices.exists(index=index_name):
        print(f"Index '{index_name}' already exists.")
        return
    
    if body is None:    # default body
        body ={
                "title": {
                    "type": "text"
                },
                "content": {
                    "type":"text"
                }
        }
    if analyzer is None:
        # standard, simple, whitespace, stop, keyword, pattern, and fingerprint
        analyzer ={
            "default": {
                "type": "standard"
            }   
        }
    # 定义索引映射和设置主分片个数
    index_mapping = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": "1",
                "analysis": {
                    "analyzer": analyzer
                }
            },
            "mappings": {
                "properties": body
            }
    }
    # 要在创建索引时配置analyzer，如索引已经创建修改analyzer需要重新创建索引
    # 索引的每个field都可以设置不同的analyzer
    try:
        es.indices.create(index=index_name, body=index_mapping)
        print(f"Index '{index_name}' created successfully with 5 primary shards.")
        # 设置alias
        # es.indices.put_alias(index='my_index', name='my_index_alias')
    except RequestError as e:
        print(e)

def test_analyzer(es, index_name):
    
    settings = es.indices.get_settings(index=index_name).get(index_name, {})
    analysis = settings.get('settings', {}).get('index', {}).get('analysis', {})
    if analysis:
        for analyzer_type, analyzers in analysis.items():
                for analyzer_name, analyzer_settings in analyzers.items():
                    print(f'  {analyzer_type}: {analyzer_name} - {analyzer_settings}')

    query = "<p>this is test for analyzer</p>"  
    analysis_result = es.indices.analyze(index=index_name,body={"text": query})

    # 提取分析结果中的分词列表
    tokens = [token_info["token"] for token_info in analysis_result["tokens"]]
    print("analyzing results", tokens)


def define_analyzer(es):
    # 定义分析器
    analyzer = {
        "analyzer": {
            "html_analyzer": {
                "type": "custom",
                "tokenizer": "smartcn",
                "char_filter": ["html_strip"]
            }
        }
    }
    return analyzer

def get_indices(es):
    # 获取集群中的所有有别名的索引
    all_indices = es.indices.get_alias(name="*")
    user_indices = {index: info for index, info in all_indices.items() if not index.startswith('.')}
    print(user_indices)
    # 获取集群中的所有索引名称
    all_indices = es.cat.indices(h="index",format="json")
    print(all_indices)
    # Get information about a specific index
    if len(all_indices)>0:
        print(es.cat.indices(index=all_indices[0]['index'], v=True))    

def get_defined_analyzer(es):
    # 获取集群中所有自定义的分析器，不包括内置分析器
    try:
        response = es.indices.get_settings(index='_all')
    except RequestError as e:
        print(e)
        return

    # 打印所有的分析器
    for index, settings in response.items():
        analysis = settings.get('settings', {}).get('index', {}).get('analysis', {})
        if analysis:
            print(f'Index: {index}')
            for analyzer_type, analyzers in analysis.items():
                for analyzer_name, analyzer_settings in analyzers.items():
                    print(f'  {analyzer_type}: {analyzer_name} - {analyzer_settings}')

def empty_es(es):

    all_indices = es.cat.indices(h="index",format="json")
    nameList = map(lambda item: item['index'], all_indices)
    for index_name in nameList:
        es.indices.delete(index=index_name, ignore=[400, 404])
        print(f"Index '{index_name}' deleted successfully.")
    

def insert_docs(es, index_name, docs):
    if isinstance(docs, dict):
        es.index(index=index_name, body=docs)
    else:
        new_docs = list(map(lambda doc:[
                                        {"index": {"_index": index_name}},
                                        doc],
                            docs))
        new_docs = sum(new_docs,[])   # Bulk可以确保所有请求以原子方式执行。这意味着所有请求要么全部成功，要么全部失败，从而确保数据的一致性
        es.bulk(index=index_name, body=new_docs) # 在索引中添加文档
    # 刷新索引，使文档立即可用
    es.indices.refresh(index=index_name)

def search(es, index_name, query):
    result = es.search(index=index_name, body={"query": {"match": {"content": query}}})
    return result


if __name__ == '__main__':
    # 连接到本地的 Elasticsearch 实例
    es = Elasticsearch(['http://localhost:9200'])
    if not es.ping():
        raise ValueError("Connection failed")
    else:
        print("Connected to Elasticsearch")

    empty_es(es)
    get_indices(es)
    sys.exit(1)

    index_name = "my_index"
    create_index(es,index_name)
    doc_count = es.count(index=index_name)['count']
    print("Number of documents in index '{}': {}".format(index_name, doc_count))

    # 插入文档
    doc =[{"title": "Elasticsearch example", "content": "This is an example of using Elasticsearch in Python"}]
    doc.append({"title": "Python", "content": "Python is a widely used programming language"})
    doc3 = {"title": "Data science with Python", "content": "Python is widely used in data science"}

    # 在索引中添加文档
    insert_docs(es, index_name, doc)
    insert_docs(es, index_name, doc3)

    doc_count = es.count(index=index_name)['count']
    print("Number of documents in index '{}': {}".format(index_name, doc_count))

    query = "python"
    result = search(es,index_name,query)
    
    # 处理搜索结果
    print("Search results for query '{}':".format(query))
    for hit in result['hits']['hits']:
        print("Score: {}, Title: {}".format(hit['_score'], hit['_source']['title']))
