from libsearch.processing.base import ParserBase

class VersionParser(ParserBase):
    parsetype = "text/plain"
    ext = "version"

    def _parse(self, f, options={}):
        version = f.read()

        return [self.createData("main","META", META_VERSION=version, META_TYPE="VERSION")]
