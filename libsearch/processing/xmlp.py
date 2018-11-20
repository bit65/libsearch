import xml.etree.ElementTree as ET
import os

from ..dbmodels import *

def parse_xml(file_name, orig_name):

    ret_data = []

    with open(file_name, "r") as file:
        file_data = file.read()

        real_path = '/' + '/'.join(file_name.split('/')[3:])
        print real_path
        print file_name
        xml_saved_data = [SaveData(data=file_data, metadata={"name": real_path})]
        ret_data.append(("XML_DATA", xml_saved_data))

    if file_name.endswith("AndroidManifest.xml"):
        root = ET.parse(file_name).getroot()
        permissions = [SaveData(data=p.attrib.items()[0][1]) for p in root.findall('uses-permission')]
            
        ret_data.append(("PERMISSIONS",permissions))

    
    
    return ret_data

    
