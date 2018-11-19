from .zip import parse_zip

def parse_apk(file_name, orig_name):
    parse_zip(file_name, orig_name)