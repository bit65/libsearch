from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
from tempfile import NamedTemporaryFile
import subprocess
from peewee import *
from playhouse.postgres_ext import *
from lxml import html
from elftools.elf.elffile import ELFFile
from cxxfilt import demangle
import requests

import os
import re

def apk_downloader(category):
    # Create cache directory if it doesn't exist
    if not os.path.exists("cache"):
        os.mkdir("cache")

    for page in range(1,100):
        # Iterate through apkpure pages to find a suitable APK
        page = requests.get('https://apkpure.com/%s?sort=new&page=%d' % (category, page))

        # Scrape HTML page to find appropriate link
        tree = html.fromstring(page.content)
        links = tree.xpath('//ul[@id="pagedata"]/li/div[@class="category-template-down"]/a')
        for link in links:
            page = requests.get('https://apkpure.com%s' % link.get("href"))
            tree = html.fromstring(page.content)
            download_link = tree.xpath('//a[@id="download_link"]')[0]
            name = tree.xpath('//div[@class="fast-download-box"]//span[@class="file"]/text()')[0].strip()
            name = re.sub('[^\w\-_\. ]', '_', name)

            # Download the APK if not already available
            try:
                if not os.path.isfile("./cache/%s" % name):
                    page = requests.get(download_link.get("href"), allow_redirects=True)
                    with open('./cache/%s' % name, 'wb') as f:
                    	f.write(page.content)

                    # Extract ZIP file and parse it
                    extract_zip(name)
                    print "Downloaded %s" % name
            except:
                print "Failed downloading %s" % name

def parse_so(file_name, orig_name):

    if orig_name.startswith("lib/"):
        _, system, name =  orig_name.split('/')

        print "LIB", system, name
    else:
        print "SO", orig_name

    with open(orig_name, "rb") as f:
        e = ELFFile(f)
        for s in e.iter_sections():
            if s['sh_type'] == 'SHT_STRTAB':
                print [demangle(x) for x in s.data().split("\x00")]
            # print(s.header)

    os._exit(0)

def parse_json(file_name, orig_name):
    print "json", orig_name

def parse_properties(file_name, orig_name):
    print "properties", orig_name

def parse_xml(file_name, orig_name):
    print "xml", orig_name

def parse_dex(file_name, orig_name):
    args = ['./ext/dexinfo/dexinfo', file_name, '-V']
    args2 = ['grep', '-oP', 'class_idx.*?L\K([^;\$]*)']

    process_dex = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    shell=False)
    process_grep = subprocess.Popen(args2, stdin=process_dex.stdout,
                                stdout=subprocess.PIPE, shell=False)
    process_dex.stdout.close()

    modules = (process_grep.communicate()[0]).splitlines()

    new_modules = [dict(data=m, metadata={}) for m in modules]

    return [
        ("MODULES",new_modules)
        ]

def parse_file(zipfile, function, file_name):
    try:
        with NamedTemporaryFile(delete=True) as temp:
            temp.write(zipfile.open(file_name).read())

            ret_modules = function(temp.name, file_name)
            if ret_modules != None:
                for name, data_list in ret_modules:
                    save_data(data_list, name, file_name)

    except Exception as e:
        print e
        pass


def extract_names(zipfile):
    for name in zipfile.namelist():
        if name.endswith(".so"):
            parse_file(zipfile, parse_so, name)

        if name.endswith(".xml"):
            parse_file(zipfile, parse_xml, name)

        if name.endswith(".json"):
            parse_file(zipfile, parse_json, name)

        if name.endswith(".properties"):
            parse_file(zipfile, parse_properties, name)

        if name.endswith(".dex"):
            parse_file(zipfile, parse_dex, name)

def extract_zip(zip_file):
    print("Extracting %s" % zip_file)

    # Extract the ZIP file form cache folder
    full_path = os.path.abspath("cache/%s" % zip_file)
    resp = urlopen(full_path)

    zipfile = ZipFile(StringIO(resp.read()))

    # Get files from zip
    new_items = [dict(data=i.filename, metadata={"crc":i.CRC}) for i in zipfile.infolist()]

    save_data(new_items, "ZIP_NAMES", zip_file)

    # Process files
    extract_names(zipfile)



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
    # dvector = TSVectorField()
    metadata = JSONField()
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


def save_data(data, type, asset):
    try:
        if isinstance(data, list):
            with psql_db.atomic():
                for d in data:
                    print d
                # try:
                #     DataDump.create(
                #         data=d["data"], 
                #         metadata=d["metadata"],
                #         dtype=type,
                #         asset=asset)
                # except Exception as e:
                #     pass
    except:
        # Just print it now
        if isinstance(data, list):
            for d in data:
                print d
