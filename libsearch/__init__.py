from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
from tempfile import NamedTemporaryFile
import subprocess
from peewee import *
from playhouse.postgres_ext import *
from lxml import html
import requests

import os
import re

def apk_downloader(category):
    for page in range(1,100):
        page = requests.get('https://apkpure.com/%s?sort=new&page=%d' % (category, page))
        tree = html.fromstring(page.content)
        links = tree.xpath('//ul[@id="pagedata"]/li/div[@class="category-template-down"]/a')
        for link in links:
            
            page = requests.get('https://apkpure.com%s' % link.get("href"))
            tree = html.fromstring(page.content)
            download_link = tree.xpath('//a[@id="download_link"]')[0]
            name = tree.xpath('//div[@class="fast-download-box"]//span[@class="file"]/text()')[0].strip()
            name = re.sub('[^\w\-_\. ]', '_', name)

            try:
                if not os.path.isfile("./cache/%s" % name):
                    page = requests.get(download_link.get("href"), allow_redirects=True)
                    open('./cache/%s' % name, 'wb').write(page.content)
                    extract_zip(name)
                    print "Downloaded %s" % name
            except:
                print "Failed downloading %s" % name 
    

def parse_dex(file_name):
    args = ['./ext/dexinfo/dexinfo', file_name, '-V']
    args2 = ['grep', '-oP', 'class_idx.*?L\K([^;\$]*)']

    process_dex = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    shell=False)
    process_grep = subprocess.Popen(args2, stdin=process_dex.stdout,
                                stdout=subprocess.PIPE, shell=False)
    process_dex.stdout.close()
    
    modules = (process_grep.communicate()[0]).splitlines()
    return [
        ("MODULES",modules)
        ]


def parse_file(zipfile, function, file_name):
    try:
        with NamedTemporaryFile(delete=True) as temp:
            temp.write(zipfile.open(file_name).read())

            for name, data_list in function(temp.name):
                save_data(data_list, name, file_name)
                
            
            # print function, file_name
    except Exception as e:
        print e
        pass


def extract_names(zipfile):
    for name in zipfile.namelist():
        if name.endswith("classes.dex"):
            parse_file(zipfile, parse_dex, name)

def extract_zip(zip_file):
    full_path = os.path.abspath("cache/"+zip_file)
    resp = urlopen(full_path)
    zipfile = ZipFile(StringIO(resp.read()))

    extract_names(zipfile)
    
    os.exit(0)

    save_data(zipfile.namelist(), "ZIP_NAMES", zip_file)



dbname="libsearch"
dbuser="postgress"
dbpassword="postgress"
dbhost="localhost"
dbport="5432"

psql_db = PostgresqlDatabase(dbname, user=dbuser, password=dbpassword, host=dbhost, port=dbport)

# class TSVectorField():
#     field_type = 'tsvector'

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

class DataDump(BaseModel):
    data = CharField(1024)
    dvector = TSVectorField()
    dtype = CharField()
    asset = CharField()
    class Meta:
        indexes = (
            # create a unique on from/to/date
            (('data', 'dtype', 'asset'), True),
        )

def init_db():
    psql_db.connect()
    psql_db.drop_tables([DataDump])
    psql_db.create_tables([DataDump])

# conn = None
# def init_db():
#     global conn


#     cs = "dbname=%s user=%s password=%s host=%s port=%s" % (dbname, dbuser, dbpassword, dbhost, dbport)

#     conn = psycopg2.connect(cs)


def save_data(data,type, asset):
    if isinstance(data, list):
        print "Saving %d %s " % (len(data), type)

        with psql_db.atomic():
            for d in set(data):
                # print type, d
                try:
                    DataDump.create(data=d, dvector=fn.to_tsvector(fn.replace(d,'/',' ')), dtype=type, asset=asset)
                except:
                    pass

    