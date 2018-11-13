from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
from tempfile import NamedTemporaryFile
import subprocess
import os



def parse_dex(file_name):
    args = ['./ext/dexinfo/dexinfo', file_name, '-V']
    args2 = ['grep', '-oP', 'class_idx.*?L\K([^;\$]*)']

    process_dex = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    shell=False)
    process_grep = subprocess.Popen(args2, stdin=process_dex.stdout,
                                  stdout=subprocess.PIPE, shell=False)
    process_dex.stdout.close()
    return process_grep.communicate()[0]
    
def extract_zip(zip_file):
    full_path = os.path.abspath("cache/"+zip_file)
    resp = urlopen(full_path)
    zipfile = ZipFile(StringIO(resp.read()))
    save_data(zipfile.namelist(), "ZIP_NAMES")

    try:
        with NamedTemporaryFile(delete=False) as temp:
            
            temp.write(zipfile.open("classes.dex").read())

            modules = parse_dex(temp.name).splitlines()
            save_data(modules, "MODULES")


            # "./dexinfo %s | grep -oP ''" % temp.name

        print buf_classes_dex
    except:
        pass
    



def save_data(data,type):
    if isinstance(data, list):
        print "Saving %d %s " % (len(data), type)
        for d in set(data):
            print type, d
    