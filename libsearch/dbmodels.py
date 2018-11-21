from peewee import *
from playhouse.postgres_ext import *
import json

__DEBUG__ONLY__ = False

dbname="libsearch"
dbuser="postgress"
dbpassword="postgress"
dbhost="localhost"
dbport="5432"

psql_db = PostgresqlDatabase(dbname, user=dbuser, password=dbpassword, host=dbhost, port=dbport)

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

class DataDump(BaseModel):
    data = CharField(4096)
    # dvector = TSVectorField()
    metadata = JSONField()
    dtype = CharField()
    asset = CharField()
    class Meta:
        indexes = (
            # create a unique on from/to/date
            (('data', 'dtype', 'asset'), True),
        )

class SaveData():
    def __init__(self, data, metadata={}):
        self.data = data[:4095]
        self.metadata = metadata

    def __str__(self):
        return "SaveData( " + self.data + "," + json.dumps(self.metadata) +" )"

    def __hash__(self):
        return hash((self.data,  json.dumps(self.metadata)))

    def data(self):
        self.data

    def metadata(self):
        self.metadata

def init_db():
    psql_db.connect()
    psql_db.drop_tables([DataDump])
    psql_db.create_tables([DataDump])

def save_data(data, type, asset):
    
    if isinstance(data, list):
        uniq_data = {}
        for d in data:
            uniq_data[d.__hash__()] = d

        with psql_db.atomic():
            print "Found %d items of %s from %s" % (len(uniq_data.items()),type, asset)

            for _,d in uniq_data.items():
                
                try:
                    if __DEBUG__ONLY__:
                        # print d, type, asset
                        pass
                    else:
                        DataDump.create(
                            data=d.data, 
                            metadata=d.metadata,
                            dtype=type,
                            asset=asset)
                except Exception as e:
                    print e
                    pass