def parse_dex(file_name, orig_name):
    args = ['./ext/dexinfo/dexinfo', file_name, '-V']
    args2 = ['grep', '-oP', 'class_idx.*?L\K([^;\$]*)']

    process_dex = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    shell=False)
    process_grep = subprocess.Popen(args2, stdin=process_dex.stdout,
                                stdout=subprocess.PIPE, shell=False)
    process_dex.stdout.close()
    
    modules = (process_grep.communicate()[0]).splitlines()

    new_modules = [SaveData(data=m) for m in modules]

    return [
        ("MODULES",new_modules)
        ]