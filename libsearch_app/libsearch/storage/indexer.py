
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import hashlib
import datetime

def xstr(s):
    if s is None:
        return ''
    return str(s)

class Indexer:
    _instance = None

    @staticmethod
    def instance():
        if Indexer._instance == None:
            Indexer._instance = Indexer()

        return Indexer._instance

    def __init__(self, index_name='libsearch_docs'):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.index_name = index_name
        self.create_index(index_name)


    def save(self, data):
        if isinstance(data, list):
            docs = [{
                    "_index": self.index_name,
                    "_type": "_doc",
                    "_id": xstr(doc['TYPE']) + xstr(doc['ASSET']) + xstr(doc['VALUE']),
                    "_source": doc
                    } for doc in data]
            before = datetime.datetime.now()
            helpers.bulk(self.es, docs)
            after = datetime.datetime.now()            
            print "Bulk Indexed %s docs in %s" % (len(docs), str(after - before))
            
            # self.save(doc)
        else:

            if ('TYPE' in data and 'ASSET' in data and 'VALUE' in data):

                id_hash = hashlib.sha256(xstr(data['TYPE']) + xstr(data['ASSET']) + xstr(data['VALUE']))
                self.es.index(index=self.index_name, id=id_hash.hexdigest(), doc_type='_doc', body=data)

    def create_index(self, index_name):
        created = False
        # index settings
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis":{
                    "analyzer":{
                        "splitter_analyzer":{ 
                            "type":"custom",
                            "tokenizer":"splitter_tokenizer",
                            "filter":[
                                "lowercase"
                            ]
                        }
                    },
                    "tokenizer": {
                        "splitter_tokenizer": {
                        "type": "char_group",
                        "tokenize_on_chars": [
                            "whitespace",
                            ".",
                            "\\",
                            "/",
                            "_",
                            ":",
                            "*",
                            "-"
                            ]
                        }
                    }
                },
            },
            "mappings": {
                "_doc": {
                    "properties": {
                        "PARENT": {
                            "type": "keyword"
                        },
                        "TYPE": {
                            "type": "keyword"
                        },
                        "ASSET": {
                            "type": "keyword"
                        },
                        "VALUE": {
                            "type": "keyword",
                            "fields": {
                                "splitted": {
                                    "type": "text",
                                    "analyzer":"splitter_analyzer"
                                }
                            }
                            
                        }
                    }
                }
            }
        }

        try:
            if not self.es.indices.exists(index_name):
                self.es.indices.create(index=index_name, ignore=400, body=settings)
            created = True
        except Exception as ex:
            print(str(ex))
        finally:
            return created
