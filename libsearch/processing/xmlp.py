from libsearch.processing.base import ParserBase
import xml.etree.ElementTree as ET
import os
import axmlparserpy.axmlprinter as axmlprinter
from StringIO import StringIO

class XMLParser(ParserBase):
    
    parsetype = ["application/octet-stream", "text/plain", "text/xml"]
    ext = "xml"

    def _parse(self, file):
        file_data = file.read()

        # Retrieve information from manifest
        if self.filename.endswith("AndroidManifest.xml"):
            ap = axmlprinter.AXMLPrinter(file_data)
            # buff = minidom.parseString(ap.getBuff()).toxml()
            # print()

            root = ET.parse(StringIO(ap.getBuff())).getroot()
            information = []

            # Get Permissions
            for p in root.findall('uses-permission'):
                information.append(
                    {
                        "VALUE": p.attrib.items()[0][1],
                        "ASSET": self.filename,
                        "TYPE": "PERMISSIONS"
                    })
                        
            # TODO - Get more stuff 

            return information
