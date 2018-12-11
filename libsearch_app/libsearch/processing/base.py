import os

parsetype = ""
ext = ""

def _uppercase_for_dict_keys(lower_dict):
    upper_dict = {}
    for k, v in lower_dict.items():
        if isinstance(v, dict):
            v = _uppercase_for_dict_keys(v)
        upper_dict[k.upper()] = v
    return upper_dict

def merge_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

class ParserBase:
    def __init__(self, filename):
        self.filename = filename
        self.filename_w = self.parent = filename.split(os.sep)[-1]

    def parse(self, fileobj = None, parent=None):
        # Choose one out of two paths:
        # 1. If no argument is given, open a file named self.filename
        # 2. If an argument is give, just pass it on.
        if parent:
            self.parent = parent

        close = False

        if fileobj is None:
            fileobj = open(self.filename, "rb")
            close = True

        ret = self._parse(fileobj)

        if close:
            fileobj.close()

        return ret
    
    def createData(self, dtype, **kwargs):
        # print "%s - %s" % (dtype, dvalue)

        return merge_dicts(_uppercase_for_dict_keys(dict(kwargs)),
                            {
                                "FILE": self.filename_w,
                                "ASSET": self.parent,
                                "TYPE": dtype
                            })