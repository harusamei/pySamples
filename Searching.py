from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import sys
from processCSV import pcsv
from datetime import datetime

def create_index(es, index_name, body_filename):
# bodyfile is csv file with the first row as the schema, second row as the type
    
    if es.indices.exists(index=index_name):
        print(f"Index '{index_name}' already exists.")
        return False
    # 读取csv构建mapping的body 
    mypcsv = pcsv()
    csv_rows = mypcsv.read_csv(body_filename,3)
    if len(csv_rows) == 0:
        return False
    
    schema = csv_rows[0]
    for key in schema.keys():
        if csv_rows[1][key] !='':
            schema[key]={"type":csv_rows[1][key]}
        else:
            schema[key]={"type":"text","analyzer":"cn_html_analyzer"}

        if schema[key]["type"]=="keyword":
            schema[key]["normalizer"] = "lowercase_normalizer"

    # 定义索引主分片个数和分析器
    index_mapping = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": "1",
                "analysis": {
                    "char_filter": {
                        "html_strip": {
                        "type": "html_strip"
                        }
                    },
                    "tokenizer": {
                        "smartcn_tokenizer": {
                        "type": "smartcn_tokenizer"
                        }
                    },
                    "analyzer": {
                        "cn_html_analyzer": {
                        "type": "custom",
                        "tokenizer": "smartcn_tokenizer",
                        "char_filter": ["html_strip"],
                        "filter": ["lowercase", "stop","cjk_width" ]
                        }
                    },
                     "normalizer": {
                        "lowercase_normalizer": {
                        "type": "custom",
                        "filter": ["lowercase"]
                        }
                    }
                }
            },
            "mappings": {
                "properties": schema
            }
    }
    # 索引的每个field都可以设置不同的analyzer
    try:
        es.indices.create(index=index_name, body=index_mapping)
        print(f"Index '{index_name}' created successfully with 5 primary shards.")
    except RequestError as e:
        print(e)
        return False
    
    return True

def get_indices(es):
    # 获取集群中的所有有别名的索引
    aliases = es.cat.aliases(format="json")
    # 过滤系统自动生成的index
    user_aliases = [alias for alias in aliases if not alias['alias'].startswith('.')]
    user_aliases = list( map(lambda alias: f"{alias['alias']}->{alias['index']}", user_aliases))
    print(f"alias -> index\n {user_aliases}")
   
    # 获取集群中的所有索引名称
    all_indices = es.cat.indices(h="index",format="json")
    print(all_indices)

def test_index(es, index_name):
    if es.indices.exists(index=index_name):
        print(es.cat.indices(index=index_name, v=True))
    else:
        print(f"Index '{index_name}' does not exist.")

def get_analyzers(es,index_name):
    # 获取映射到index的analyzer，不包括内置分析器
    settings = es.indices.get_settings(index=index_name).get(index_name, {})
    analysis = settings.get('settings', {}).get('index', {}).get('analysis', {})
    if analysis:
        print(f'Index: {index_name}')
        for analyzer_type, analyzers in analysis.items():
            for analyzer_name, analyzer_settings in analyzers.items():
                print(f'  {analyzer_type}: {analyzer_name} - {analyzer_settings}')
    else:
        print(f'No custom analyzers found for index {index_name}')

def test_analyzer(es, index_name):
    
    query = "<p>this is test for analyzer, 我有一个好朋友</p>"  
    analysis_result = es.indices.analyze(index=index_name, body={"analyzer": "cn_html_analyzer", "text": query})

    # 提取分析结果中的分词列表
    tokens = [token_info["token"] for token_info in analysis_result["tokens"]]
    print("analyzing results", tokens)

# 格式规范化
def format_doc(doc):

    delkeys = []
    for key in doc.keys():
        if doc[key] == '':
           delkeys.append(key)
    for key in delkeys:
        del doc[key]
       
    date_str = doc['time_to_market']
    date_obj = datetime.strptime(date_str, '%Y/%m/%d')
    doc['time_to_market'] = date_obj.strftime('%Y-%m-%d')


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

def delete_doc(es, index_name, doc_id):
    
    exists = es.exists(index=index_name, id=doc_id)
    if exists:
        es.delete(index=index_name, id=doc_id)
    es.indices.refresh(index=index_name)

def update_doc_field(es, index_name, doc_id, field, new_value):
    body = {
        "doc": {
            field: new_value
        }
    }
    res = es.update(index=index_name, id=doc_id, body=body)
    es.indices.refresh(index=index_name)
    return res

def get_count(es, index_name):
    count = es.count(index=index_name)['count']
    return count

def search(es, index_name, qbody):
    result = es.search(index=index_name, body={"query": {"match": qbody}})
    return result

def get_docids(result):
    docids = []
    for hit in result['hits']['hits']:
        docids.append(hit['_id'])
    return docids


if __name__ == '__main__':
    # 连接到本地的 Elasticsearch 实例
    es = Elasticsearch(['http://localhost:9200'],
                       basic_auth=('elastic', 'a3ghnRyzop2O1B2yOnqT'))
    if not es.ping():
        raise ValueError("Connection failed")
    else:
        print("Connected to Elasticsearch")

   
    index_name = "leproducts1"

    qbody = {'uid':"11"}
    result = search(es,index_name,qbody)
    print(get_docids(result))
    print(result)
    
    res = update_doc_field(es, index_name, "T2ShO44BGnk_J1z3f7c0", "price", "345")
    print(res)
    result = search(es,index_name,qbody)
    print(result)
