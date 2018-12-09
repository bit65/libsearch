from libsearch.processing.base import ParserBase
from libsearch.processing.searchparser import Parser as P
from zipfile import ZipFile
import datetime
from androguard.core.bytecodes.axml import AXMLPrinter
from androguard.core.bytecodes.axml import ARSCParser
from androguard.core.bytecodes.axml import get_arsc_info
import re
import lxml.etree
from unidecode import unidecode

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

    def extract_all_attributes(self, element):
        ret_attr = []
        for k, v in element.attrib.items():
            k = re.sub('\{.*\}', '', k)
            if self.resource_parser and v and v[0] == '@':
                v = self.resource_parser.resource_values[int(v[1:], 16)].values()[0].get_value()

            ret_attr.append((k, v))
        return ret_attr


    def _parse(self, f):
        print "Parsing APK"

        information = []
        zipfile = ZipFile(f)

        # try:
        skip_android_assets = False

        if 'AndroidManifest.xml' in zipfile.namelist() and 'resources.arsc' in zipfile.namelist():
            manifest_file = zipfile.read('AndroidManifest.xml')
            resources_file = zipfile.read('resources.arsc')
            information += self.parse_manifest(manifest_file, resources_file)
            skip_android_assets = True

        for x in zipfile.infolist():
            # Add File to index
            if skip_android_assets and (x.filename == 'AndroidManifest.xml' or x.filename == 'resources.arsc'):
                continue

            data = self.createData("FILE", x.filename)
            data["CRC"] = x.CRC
            information.append(data)

            # Process File
            parser = P.instance().get_parser(x.filename)

            if parser is None:
                continue

            try:
                before = datetime.datetime.now()
                results = parser.parse(zipfile.open(x.filename), parent=self.filename_w)
                after = datetime.datetime.now()
                if (after - before) > datetime.timedelta(seconds=1):
                    print "Parsed %s in %s" % (x.filename, str(after - before))

                if results is not None:
                    information += results

            except Exception as e:
                print "Cannot process %s" % x.filename
                print e

        return information

    def parse_manifest(self, manifest_file, resource_file):
        information = []



        print "Parsing Resource XML"
        self.resource_parser = arcParser = ARSCParser(resource_file)


        for p in arcParser.get_packages_names():
            information.append(self.createData("APK-PACKAGES", p))

            for locale in arcParser.get_locales(p):
                for t in arcParser.get_types(p, locale):
                    for x in arcParser.values[p][locale][t]:
                        try:
                            if t == "public":
                                (type, value, id) = x

                                if isinstance(value, unicode):
                                    value = unidecode(value)

                                information.append(self.createData("APK-RESOURCE-PUBLIC", value, locale=locale, package=p, restype=t, type=type, id=id))
                            elif len(x) == 2:
                                (key, value) = x

                                # print "TypeB", type(value)
                                if isinstance(value, unicode):
                                    value = unidecode(value)

                                information.append(
                                    self.createData("APK-RESOURCE-" + t.upper(), value, locale=locale, package=p, restype=t,
                                                    key=key))
                            else:
                                value = x[0]
                                if isinstance(value, unicode):
                                    value = unidecode(value)

                                information.append(
                                    self.createData("APK-RESOURCE-" + t.upper(), value, locale=locale, package=p, restype=t))
                        except Exception as e:
                            print x
                            print e


        print "Parsing Manifest XML"
        xmlPrinter = AXMLPrinter(manifest_file)

        root = xmlPrinter.get_xml_obj()


        # Get Permissions
        for p in root.findall('uses-permission'):
            attribute = self.extract_attribute(p, 'name')
            if attribute:
                information.append(self.createData("APK-PERMISSIONS", attribute))

        for p in root.findall('uses-feature'):
            attribute = self.extract_attribute(p, 'name')
            if attribute:
                information.append(self.createData("APK-FEATURE", attribute))

        app = root.find('application')
        for p in app.findall('activity'):
            attribute = self.extract_attribute(p, 'name')
            for intent in p.findall('intent-filter'):
                action = self.extract_attribute(intent.find('action'), 'name')

                for c in intent.findall('category'):
                    category = self.extract_attribute(c, 'name')
                    information.append(
                        self.createData("APK-ACTIVITY", attribute, action=action, category=category))

                for c in intent.findall('data'):
                    host = self.extract_attribute(c, 'host')
                    scheme = self.extract_attribute(c, 'scheme')
                    information.append(self.createData("APK-ACTIVITY", attribute, action=action, host=host, scheme=scheme))

        for e in app.findall('uses-library'):
            lib = self.extract_attribute(e, 'name')
            information.append(self.createData("APK-USES-LIB", lib))

        for e in app.findall('meta-data'):
            name = self.extract_attribute(e, 'name')
            value = self.extract_attribute(e, 'value')
            information.append(self.createData("APK-META", value, name=name))

        for e in app.findall('receiver'):
            attributes = self.extract_all_attributes(e)
            name = self.extract_attribute(e, 'name')
            data = self.createData("APK-RECIEVER",name)
            for attr, value in attributes:
                if attr == "exported":
                    data["EXPORTED"] = value
                if attr == "permission":
                    data["PERMISSION"] = value
                if attr == "enabled":
                    data["ENABLED"] = value

            information.append(data)

            for intent in e.findall('intent-filter'):
                for a in intent.findall('action'):
                    action = self.extract_attribute(a, 'name')
                    information.append(self.createData("APK-RECIEVER-ACTION", action, reciever=name))


        attributes = self.extract_all_attributes(app)
        for attr, value in attributes:
            information.append(self.createData("APK-ATTR-%s" % attr.upper(), value))


        return information
