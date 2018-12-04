from libsearch.processing.base import ParserBase
import xml.etree.ElementTree as ET
import os
# import axmlparserpy.axmlprinter as axmlprinter
from androguard.core.bytecodes.axml import AXMLPrinter
from StringIO import StringIO
import re
import code

def extract_attribute(element, attribute):
    for i in element.attrib.items():
        if i[0].endswith(attribute):
            return i[1]
    return

def extract_all_attributes(element):
    ret_attr = []
    for k, v in element.attrib.items():
        k = re.sub('\{.*\}', '', k)
        ret_attr.append((k,v))
    return ret_attr

class XMLParser(ParserBase):
    
    parsetype = ["application/octet-stream", "text/plain", "text/xml"]
    ext = "xml"

    def _parse(self, file):
        
        file_data = file.read()

        # Retrieve information from manifest
        if self.filename.endswith("AndroidManifest.xml"):
            ap = AXMLPrinter(file_data)
            
            
            # root = ET.parse(StringIO(ap.getBuff())).getroot()
            root = ap.get_xml_obj()
            information = []

            # Get Permissions

            
            
            for p in root.findall('uses-permission'):
                attribute = extract_attribute(p,'name')
                if attribute:
                    information.append(self.createData("APK-PERMISSIONS",attribute))

            for p in root.findall('uses-feature'):
                attribute = extract_attribute(p,'name')
                if attribute:
                    information.append(self.createData("APK-FEATURE",attribute))

            app = root.find('application')
            for p in app.findall('activity'):
                attribute = extract_attribute(p,'name')
                if attribute:
                    information.append(self.createData("APK-FEATURE",attribute))
            
            # for p in app.findall('category'):
            #     attribute = extract_attribute(p,'name')
            #     if attribute:
            #         information.append(self.createData("APK-CAT",attribute))


            for p in app.findall('receiver'):
                attributes = extract_all_attributes(p)
                # print attributes
                data = self.createData("APK-RECIEVER")
                for attr, value in attributes:
                    # print attr, value
                    if attr == "name":
                        data["VALUE"] = value
                    if attr == "exported":
                        data["EXPORTED"] = value
                    if attr == "permission":
                        data["PERMISSION"] = value
                    if attr == "enabled":
                        data["ENABLED"] = value

                information.append(data)
            
                # attribute = extract_attribute(p,'name')
                # if attribute:
                #     information.append(self.createData("APK-PERMISSIONS",attribute))
            return information

            attributes = extract_all_attributes(app)
            for attr, value in attributes:
                if value[0] != '@' and value[0:2] != '0x':
                    information.append(self.createData("APK-ATTR-%s" % attr.upper() ,value))
                        # print attr, value
                # if attribute:
                #     information.append(self.createData("APK-FEATURE",attribute))

                        
            
            # for p in root.findall('permission'):
            #     information.append(self.createData("APK-PERMISSIONS",p.attrib.items()[0][1]))

            # for p in root.findall('uses-feature'):
            #     information.append(self.createData("APK-FEATURES",p.attrib.items()[0][1]))
                        
            # TODO - Get more stuff 

            return information
