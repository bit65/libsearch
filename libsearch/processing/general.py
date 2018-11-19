from tempfile import NamedTemporaryFile
from ..dbmodels import *

def parse_file(zipfile, function, file_name):
    try:
        with NamedTemporaryFile(delete=True) as temp:
            temp.write(zipfile.open(file_name).read())

            ret_modules = function(temp.name, file_name)
            if ret_modules != None:
                for name, data_list in ret_modules:
                    save_data(data_list, name, file_name)
                
    except Exception as e:
        print e
        pass