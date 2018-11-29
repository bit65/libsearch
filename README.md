# QUICK INSTALL

git submodule init
git submodule update

make -C ./ext/dexinfo/
pip install -e .

wget https://github.com/iBotPeaches/Apktool/releases/download/v2.3.4/apktool_2.3.4.jar -o ./ext/apktool.jar

# TESTS
python -m unittest libsearch.tests.test_processing.TestProcessing

# RUN EXAMPLE
./examples/searcher.py

# SYNC ElasticSearch with postgress
Install abc - https://github.com/appbaseio/abc

abc import --src_type=postgres --src_uri="postgresql://postgress:postgress@127.0.0.1:5432/libsearch" "http://localhost:9200/libsearch"

# Prepare lucene indexer
https://repo.maven.apache.org/maven2/.index/nexus-maven-repository-index.gz
https://repo.maven.apache.org/maven2/org/apache/maven/indexer/indexer-cli/6.0.0/indexer-cli-6.0.0.jar
java -jar indexer-cli-6.0.0.jar --unpack nexus-maven-repository-index.gz --destination central-lucene-index --type full