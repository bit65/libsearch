from os import listdir, path
import inspect
import imp
from magic import Magic, MAGIC_MIME_TYPE
from base import ParserBase

class Parser:
    _instance = None

    @staticmethod
    def instance():
        if Parser._instance == None:
            Parser._instance = Parser()

        return Parser._instance

    parsers = {}

    def __init__(self):
        self.m = Magic(flags = MAGIC_MIME_TYPE)

        for filename in listdir(path.dirname(__file__)):
            if filename in __file__:
                continue

            if filename.endswith(".py") and not filename.startswith("_"):
                # print filename[:-3], path.sep.join([path.dirname(__file__), filename])
                m = imp.load_source(filename[:-3], path.sep.join([path.dirname(__file__), filename]))

                for member in dir(m):
                    if member is "ParserBase":
                        continue
                    cls = getattr(m, member)
                    if inspect.isclass(cls) and issubclass(cls, ParserBase):
                        self.register(cls, cls.ext)


    def __del__(self):
        self.m.close()

    def register(self, parser, ext):
        # print "Registering [%s][%s]" % (mimetypes, ext), parser.parse
        if type(ext) == list:
            for e in ext:
                Parser.parsers[e] = parser
        else:
            Parser.parsers[ext] = parser

    def get_parser(self, filename):
        name, ext = path.splitext(filename)

        if ext[1:] in Parser.parsers:
            return Parser.parsers[ext[1:]](filename)

        return None
