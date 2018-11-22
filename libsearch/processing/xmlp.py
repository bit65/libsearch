from libsearch.processing.base import ParserBase
import xml.etree.ElementTree as ET
import os
import axmlparserpy.axmlprinter as axmlprinter
from StringIO import StringIO

class XMLParser(ParserBase):
    
    parsetype = ["application/octet-stream", "text/plain", "text/xml"]
    ext = "xml"

    def parse(self, file_name):
        with open(file_name, "r") as file:
            filename_w_ext = os.path.basename(file_name)
            file_data = file.read()
            
            # Retrieve information from manifest
            if filename_w_ext.endswith("AndroidManifest.xml"):
                ap = axmlprinter.AXMLPrinter(open(file_name, 'rb').read())
                # buff = minidom.parseString(ap.getBuff()).toxml()
                # print()

                root = ET.parse(StringIO(ap.getBuff())).getroot()
                information = []

                # Get Permissions
                for p in root.findall('uses-permission'):
                    information.append(
                        {
                            "VALUE": p.attrib.items()[0][1],
                            "ASSET": filename_w_ext,
                            "TYPE": "PERMISSIONS"
                        })
                        
                # TODO - Get more stuff 

                return information
