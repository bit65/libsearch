#!/usr/bin/env python
# encoding: utf-8


from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import helpers
import hashlib
import datetime
import os

def xstr(s):
    if s is None:
        return ''
    return unicode(s)


class Indexer:
    _instance = None

    @staticmethod
    def instance(options=None):
        
        if options == None:
            host = os.getenv('ES_HOST', "localhost")
            port = os.getenv('ES_PORT', 9200)
            ssl = os.getenv('SSL', False)

            if ssl == False:
                options = {'hosts': [{'host': host, 'port': port}]}
            else:
                options = {'hosts': [{'host': host, 'port': port}],
                            'use_ssl': True,
                            'verift_certs': True,
                            'connection_class': RequestsHttpConnection
                            }
    
        if Indexer._instance == None:
            Indexer._instance = Indexer(options=options)

        return Indexer._instance

    def __init__(self, options, index_name='libsearch_docs'):
        self.es = Elasticsearch(**options)
        self.index_name = index_name
        # self.create_index(index_name)

    def _prepare_doc(self,doc):
        index = self.index_name

        if 'INDEX' in doc:
            index = 'index_'+ doc['INDEX'].lower()
            del doc['INDEX']            

        id_hash = hashlib.sha256(str(doc.items())).hexdigest()

        return {
                    "_index": index,
                    "_type": '_doc',
                    "_id": id_hash,
                    "_source": doc
                }

    def save(self, data):
        if isinstance(data, list):

            docs = [self._prepare_doc(doc) for doc in data]
            
            before = datetime.datetime.now()
            helpers.bulk(self.es, docs)
            after = datetime.datetime.now()
            print "Bulk Indexed %s docs in %s" % (len(docs), str(after - before))
        else:
            self.save([data])

    def create_index(self, index_name):
        created = False
        # index settings
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
            },
            "mappings": {   
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
