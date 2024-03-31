import sys
sys.path.insert(0, 'c:/something/pySamples')
import unittest
from elasticsearch import Elasticsearch
from esIndex import create_index,insert_docs

class TestESIndex(unittest.TestCase):
    es = None
    def setUp(self):

        self.es = Elasticsearch(['http://localhost:9200'],
                       basic_auth=('elastic', 'a3ghnRyzop2O1B2yOnqT'))
        if not self.es.ping():
            raise ValueError("Connection failed")
        else:
            print("Connected to Elasticsearch")

        

    def test_index_creation(self):
        # Test if the index is created successfully
        index_name = "my_index"
        data_filename = "data\pSch.csv"
        create_index(self.es, index_name,data_filename)

    def test_document_indexing(self):
        # Test if a document is indexed successfully
        index_name = "my_index"
        document = {
            "title": "Test Document",
            "content": "This is a test document"
        }
        insert_docs(self.es, index_name, document)

    

if __name__ == '__main__':
    unittest.main()
