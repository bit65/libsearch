from os import listdir, path
import inspect
import imp
from magic import Magic, MAGIC_MIME_TYPE
from libsearch.storage.indexer import Indexer

class Parser:
    parsers = {}

    def __init__(self):
        self.indexer = Indexer()
        self.m = Magic(flags = MAGIC_MIME_TYPE)

        for filename in listdir(path.dirname(__file__)):
            if filename in __file__:
                continue

            if filename.endswith(".py"):
                m = imp.load_source(filename[:-3], path.sep.join([path.dirname(__file__), filename]))

                for member in filter(lambda x: "Parser" in x and "ParserBase" not in x and getattr(getattr(m, x), "parse") is not None, dir(m)):
                    cls = getattr(m, member)
                    if inspect.isclass(cls):
                        # print m, cls
                        parser = cls(self)

                        self.register(parser, cls.parsetype, cls.ext)

    def __del__(self):
        self.m.close()

    def register(self, parser, mimetypes, ext):
        # print "Registering [%s][%s]" % (mimetypes, ext), parser.parse
        if type(mimetypes) == list:
            for mimetype in mimetypes:
                if mimetype not in Parser.parsers:
                    Parser.parsers[mimetype] = {}

                Parser.parsers[mimetype][ext] = parser
        else:
            if mimetypes not in Parser.parsers:
                Parser.parsers[mimetypes] = {}

            Parser.parsers[mimetypes][ext] = parser

    def parse(self, filename, index=False):
        name, ext = path.splitext(filename)
        mime = self.m.id_filename(filename)

        results = Parser.parsers[mime][ext[1:]].parse(filename)
        if index:
            self.indexer.save(results)
        return results

        
