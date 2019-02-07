#!/usr/bin/env python
# encoding: utf-8

import os
from libsearch.storage.indexer import Indexer
from libsearch.enrichment.module_mapper import ModuleMapper

indexer = Indexer.instance()

query = {
  "size": 0,
  "aggs": {
    "modules": {
      "terms": {
        "field": "MODULE_NAME.keyword",
        "size": 10000
      },
      "aggs": {
        "apps": {
          "terms": {
            "field": "ASSET.keyword"
          }
        }
      }
    }
  }
}

information = []

modules_apps = indexer.search_agg(query, "modules", "apps")
libs_modules = ModuleMapper.instance().search_all(modules_apps.keys())

for l in libs_modules:
    l["full_artifact"] = "%s.%s" % (l["groupId"],l["artifactId"])

    index_lib_dict = {'INDEX_LIBRARY_'+k.upper(): v for k, v in l.items() if "module" not in k}
    index_lib_dict["TYPE"] = "INDEX_LIBRARY"
    information.append(dict(index_lib_dict))
    
    lib_dict = {'LIBRARY_'+k.upper(): v for k, v in l.items() if "module" not in k}
    lib_dict["TYPE"] = "LIBRARY"
    lib_dict["FILE"] = "NONE"

    for app in modules_apps[l['actual_module']]:
        lib_dict["ASSET"] =  app
        information.append(dict(lib_dict))
    


    # information.append(self.createData("main", "LIBRARY", **{'LIBRARY_'+k.upper(): v for k, v in l.items()}))
    

indexer.save(information)
# modules_found = [l['module'] for l in libs]

# modules = sorted(modules)

# print modules


# for m in modules:
#     if m.startswith(tuple(modules_found)):
#         print "FOUND", m


# for m in modules:
#     if not m.startswith(tuple(modules_found)):
#         print "MISSING", m