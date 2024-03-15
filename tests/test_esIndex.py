import unittest
from searching import eSearch
class TestESIndex(unittest.TestCase):
    def setUp(self):
        self.es = Elasticsearch()

    def test_index_creation(self):
        # Test if the index is created successfully
        index_name = "my_index"
        self.es.indices.create(index=index_name)
        self.assertTrue(self.es.indices.exists(index=index_name))

    def test_document_indexing(self):
        # Test if a document is indexed successfully
        index_name = "my_index"
        document = {
            "title": "Test Document",
            "content": "This is a test document"
        }
        self.es.index(index=index_name, body=document)
        self.assertTrue(self.es.exists(index=index_name, id=1))

    def tearDown(self):
        # Clean up the index after each test
        index_name = "my_index"
        self.es.indices.delete(index=index_name, ignore=[400, 404])

if __name__ == '__main__':
    unittest.main()
