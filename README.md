# QUICK INSTALL

git submodule init
git submodule update

make -C ./ext/dexinfo/
pip install -e .

# RUN EXAMPLE

./examples/searcher.py

# SYNC ElasticSearch with postgress
Install abc - https://github.com/appbaseio/abc

abc import --src_type=postgres --src_uri="postgresql://postgress:postgress@127.0.0.1:5432/libsearch" "http://localhost:9200/libsearch"