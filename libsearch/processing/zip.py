import os
from StringIO import StringIO
from urllib import urlopen
from zipfile import ZipFile

from ..dbmodels import *
from .general import parse_file

from .xml import parse_xml
from .so import parse_so
from .properties import parse_properties
from .json import parse_json
from .dex import parse_dex


def parse_zip(file_name, orig_name):
    full_path = os.path.abspath(file_name)
    resp = urlopen(full_path)
    zipfile = ZipFile(StringIO(resp.read()))

    # Get files from zip
    new_items = [SaveData(data=i.filename, metadata={"crc":i.CRC}) for i in zipfile.infolist()]
    save_data(new_items, "ZIP_NAMES", file_name)

    # Process files inside zip
    extract_names(zipfile)
    
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

        if name.endswith(".zip") or name.endswith(".apk"):
            parse_file(zipfile, parse_zip, name)
