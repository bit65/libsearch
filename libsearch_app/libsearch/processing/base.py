import os
from libsearch.storage.indexer import Indexer
import requests
from io import BytesIO

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

class NetFile():
    def __init__(self, url):
        self.url = url
        self.pos = 0
        headers = {"Range": "bytes=0-2"}
        page = requests.get(self.url, allow_redirects=True, headers=headers)
        self.url = page.url
        self.size = int(page.headers['Content-Range'].split('/')[1])
        
    def seek(self, cookie, whence):
        if whence == 0:
            self.pos = cookie
        if whence == 1:
            self.pos = self.pos + cookie
        if whence == 2:
            self.pos = self.size + cookie

        # print "new pos", self.pos

    def tell(self):
        # print "tell pos", self.pos
        return self.pos

    def read(self, n=None):
        
        newpos = 0
        if n is None:
            newpos = self.size
            headers = {"Range": "bytes=%d-" % (self.pos)}
        else:
            newpos = self.pos+n
            headers = {"Range": "bytes=%d-%d" % (self.pos, newpos-1)}

        r = requests.get( self.url, allow_redirects=True, headers=headers)
        
        self.pos = newpos

        return BytesIO(r.content).read()

class ParserBase:
    def __init__(self, filename):
        self.filename = filename
        self.filename_w = self.parent = filename.split(os.sep)[-1]

    def parse(self, fileobj = None, parent=None, save=False):
        # Choose one out of two paths:
        # 1. If no argument is given, open a file named self.filename
        # 2. If an argument is give, just pass it on.
        if parent:
            self.parent = parent

        close = False

        if type(fileobj) is str and (fileobj.startswith('https://') or fileobj.startswith('http://')):
            fileobj = NetFile(fileobj)

        if fileobj is None:
            fileobj = open(self.filename, "rb")
            close = True

        ret = self._parse(fileobj)

        if close:
            fileobj.close()
        
        if save:
            Indexer.instance().save(ret)

        return ret
    
    def createData(self, dindex, dtype, **kwargs):
        # print "%s - %s" % (dtype, dvalue)

        return merge_dicts(_uppercase_for_dict_keys(dict(kwargs)),
                            {
                                "FILE": self.filename_w,
                                "ASSET": self.parent,
                                "TYPE": dtype,
                                "INDEX": dindex
                            })