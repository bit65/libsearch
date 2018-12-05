# QUICK INSTALL

mkdir /opt && cd /opt && git clone https://github.com/bit65/libsearch


cd /opt/libsearch && git submodule init && git submodule update

cd /opt/libsearch/libsearch_app && pip install -e .


# Install pydexinfo
<!-- make -C ./ext/dexino/ -->
cd /opt/libsearch/libsearch_app/ext/dexinfo && make && pip install -e .

# Install PyLucene
sudo apt-get install -y default-jdk ant

curl https://www.apache.org/dist/lucene/pylucene/pylucene-7.5.0-src.tar.gz \
    | tar -xz --strip-components=1

sudo apt install openjdk-8-jdk-headless

cd jcc && sudo JCC_JDK=/usr/lib/jvm/default-java python setup.py install

make all install JCC='python -m jcc' ANT=ant PYTHON=python NUM_FILES=8

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