from libsearch.processing.base import ParserBase
from libsearch.processing.searchparser import Parser as P
from zipfile import ZipFile
import datetime
from androguard.core.bytecodes.axml import AXMLPrinter
from androguard.core.bytecodes.axml import ARSCParser
from androguard.core.bytecodes.axml import get_arsc_info
import re
from lxml import etree
from lxml import objectify

from collections import defaultdict
from unidecode import unidecode

def merge_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

class APKParser(ParserBase):
    parsetype = "application/zip"
    ext = "apk"
    resource_parser = None

    def extract_attribute(self, element, attribute):

        attr = None
        for i in element.attrib.items():
            if i[0].endswith(attribute):
                attr = i[1]

        if self.resource_parser and attr and attr[0] == '@':
            attr = self.resource_parser.resource_values[int(attr[1:], 16)].values()[0].get_value()

        return attr

    def extract_all_attributes(self, element, func=None, override=False, prefix=""):
        ret_attr = {}
        for k, v in element.attrib.items():
            k = re.sub('^\{.*\}', '', k)
            if self.resource_parser and v and v[0] == '@':
                try:
                    hex_value = int(v[1:], 16)
                    v = self.resource_parser.resource_values[hex_value].values()[0].get_value()
                except ValueError:
                    pass

            if func is not None:
                ret_attr = merge_dicts(ret_attr, func(k,v))
            
            if override == False:
                ret_attr[prefix + k] = v
            
        return ret_attr


    def _parse(self, f):
        print "Parsing APK"

        information = []
        zipfile = ZipFile(f)

        skip_android_assets = False

        if 'AndroidManifest.xml' in zipfile.namelist():
            resources_file = None
            manifest_file = zipfile.read('AndroidManifest.xml')

            if 'resources.arsc' in zipfile.namelist():
                resources_file = zipfile.read('resources.arsc')
    
            information += self.parse_manifest(manifest_file, resources_file)
            skip_android_assets = True

        for x in zipfile.infolist():
            # Add File to index
            if skip_android_assets and (x.filename == 'AndroidManifest.xml' or x.filename == 'resources.arsc'):
                continue

            information.append(self.createData("main", "FILE", FILE_NAME=x.filename, FILE_CHECKSUM=x.CRC))

            # Process File
            parser = P.instance().get_parser(x.filename)

            if parser is None:
                continue

            try:
                results = parser.parse(zipfile.open(x.filename), parent=self.filename_w)

                if results is not None:
                    information += results

            except Exception as e:
                print "Cannot process %s" % x.filename
                import traceback
                print(traceback.format_exc())

        return information

    def parse_manifest(self, manifest_file, resource_file):
        information = []

        apk_info = defaultdict(list)
        print "Parsing Resource XML"
        if resource_file is not None:
            self.resource_parser = arcParser = ARSCParser(resource_file)
            for p in arcParser.get_packages_names():
                apk_info['packages'].append(p)

                for locale in arcParser.get_locales(p):
                    for t in arcParser.get_types(p, locale):
                        for x in arcParser.values[p][locale][t]:
                            try:
                                if t == "public":
                                    (type, value, id) = x

                                    if isinstance(value, unicode):
                                        value = unidecode(value)
                                    
                                    information.append(self.createData("main", "RESOURCE", 
                                        RESOURCE_VALUE=value, RESOURCE_LOCALE=locale, RESOURCE_PACKAGE=p, RESOURCE_TYPE=t, RESOURCE_TYPE2=type, RESOURCE_ID=id))
                                elif len(x) == 2:
                                    (key, value) = x

                                    if isinstance(value, unicode):
                                        value = unidecode(value)

                                    information.append(
                                        self.createData("main", "RESOURCE", RESOURCE_VALUE=value, RESOURCE_LOCALE=locale, RESOURCE_PACKAGE=p, RESOURCE_TYPE=t,
                                                        RESOURCE_KEY=key))
                                else:
                                    value = x[0]
                                    if isinstance(value, unicode):
                                        value = unidecode(value)

                                    information.append(
                                        self.createData("main", "RESOURCE", RESOURCE_VALUE=value, RESOURCE_LOCALE=locale, RESOURCE_PACKAGE=p, RESOURCE_TYPE=t))
                            except Exception as e:
                                print x
                                print e

        print "Parsing Manifest XML"
        xmlPrinter = AXMLPrinter(manifest_file)

        root = xmlPrinter.get_xml_obj()

        
        # Get Permissions
        for e in root.findall('uses-permission'):
            attributes = self.extract_all_attributes(e, func=permissions_func, override=True)
            information.append(self.createData("main", "PERMISSION", **{'PERMISSION_'+k.upper(): v for k, v in attributes.items()}))

        
        
        for e in root.findall('uses-permission-sdk-23'):
            attributes = self.extract_all_attributes(e, func=permissions_func, override=True)
            information.append(self.createData("main", "PERMISSION", **{'PERMISSION_'+k.upper(): v for k, v in attributes.items()}))
        

        for e in root.findall('uses-feature'):
            attributes = self.extract_all_attributes(e)
            information.append(self.createData("main", "FEATURES", **{'FEATURES_'+k.upper(): v for k, v in attributes.items()}))


        app = root.find('application')
        attributes = self.extract_all_attributes(app)
        information.append(self.createData("main", "APP", **{'APP_'+k.upper(): v for k, v in attributes.items()}))

        if app is not None:
            for e in app.findall('.//meta-data'):
                attributes = self.extract_all_attributes(e)
                information.append(self.createData("main", "META" ,**{'META_'+k.upper(): v for k, v in attributes.items()}))

            # for e in app.findall('uses-library'):
            #     attributes = self.extract_all_attributes(e)
            #     information.append(self.createData("main", "APK-USES-LIB" ,**attributes))

            for tagtype in ['activity', 'receiver', 'service']:
                for e in app.findall(tagtype):
                    attributes = self.extract_all_attributes(e)
                    information.append(self.createData("main", tagtype.upper() ,**{tagtype.upper()+'_'+k.upper(): v for k, v in attributes.items()}))

                    for intent in e.findall('intent-filter'):
                        intentions = defaultdict(list)
                        for e2 in intent.getchildren():
                            # print e2.tag
                            attributes = self.extract_all_attributes(e2, prefix=e2.tag +".")
                            for k,v in attributes.iteritems():
                                intentions[tagtype.upper() + "_" + k].append(v)

                        information.append(self.createData("main", tagtype.upper() ,**intentions))

        return information

def permissions_func(k,v):

    ret_dict = {}

    if v.find("android.permission.") == 0:
        ret_dict[k] = v[len("android.permission."):]
        ret_dict['default'] = True
    else:
        # ret_dict['android_permission'] = False
        ret_dict[k] = v.split('.')[-1]
        ret_dict['parent'] = ".".join(v.split('.')[:-1])
        ret_dict['default'] = False

    return ret_dict