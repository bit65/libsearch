import os
from StringIO import StringIO
from urllib import urlopen
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
from base import ParserBase
import zip as zipparse

from magic import Magic, MAGIC_MIME_TYPE

class APKParser(zipparse.ZIPParser):
    parsetype = "application/zip"
    ext = "apk"
