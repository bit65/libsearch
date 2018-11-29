parsetype = ""
ext = ""

class ParserBase:
    def __init__(self, filename):
        self.filename = filename

    def parse(self, fileobj = None):
        # Choose one out of two paths:
        # 1. If no argument is given, open a file named self.filename
        # 2. If an argument is give, just pass it on.

        close = False

        if fileobj is None:
            fileobj = open(self.filename, "rb")
            close = True

        ret = self._parse(fileobj)

        if close:
            fileobj.close()

        return ret
