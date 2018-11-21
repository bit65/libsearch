from os import listdir, path
import inspect
import imp
from magic import Magic, MAGIC_MIME_TYPE

class Parser:
    parsers = {}

    def __init__(self):
        self.m = Magic(flags = MAGIC_MIME_TYPE)

        for filename in listdir(path.dirname(__file__)):
            if filename in __file__:
                continue

            if filename.endswith(".py"):
                m = imp.load_source(filename[:-3], path.sep.join([path.dirname(__file__), filename]))

                for member in filter(lambda x: "Parser" in x, dir(m)):
                    if member == "ParserBase":
                        continue

                    cls = getattr(m, member)
                    if inspect.isclass(cls):
                        obj = cls(self)
                        self.register(obj, m.parsetype, m.ext)

    def __del__(self):
        self.m.close()

    def register(self, parser, mimetypes, ext):

        if type(mimetypes) == list:
            for mimetype in mimetypes:
                if mimetype not in Parser.parsers:
                    Parser.parsers[mimetype] = {}

                Parser.parsers[mimetype][ext] = parser.parse
        else:
            if mimetypes not in Parser.parsers:
                Parser.parsers[mimetypes] = {}

            Parser.parsers[mimetypes][ext] = parser.parse

    def parse(self, filename):
        name, ext = path.splitext(filename)
        mime = self.m.id_filename(filename)
        
        results = Parser.parsers[mime][ext[1:]](filename)
        
        # Save Results
        
        return results

