def parse_so(file_name, orig_name):

    if orig_name.startswith("lib/"):
        _, system, name =  orig_name.split('/')
        
        print "LIB", system, name
    else: 
        print "SO", orig_name
