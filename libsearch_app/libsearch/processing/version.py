from libsearch.processing.base import ParserBase

class VersionParser(ParserBase):
    parsetype = "text/plain"
    ext = "version"

    def _parse(self, f):
        version = f.read()
        return [self.createData("meta","version", version=version)]
