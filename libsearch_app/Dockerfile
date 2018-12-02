FROM python:2.7

######## PYLUCENE ########

WORKDIR /usr/src/pylucene

RUN apt-get update \
    && apt-get install -y default-jdk ant
    
RUN curl https://www.apache.org/dist/lucene/pylucene/pylucene-7.5.0-src.tar.gz \
    | tar -xz --strip-components=1
RUN cd jcc \
    && JCC_JDK=/usr/lib/jvm/default-java python setup.py install
RUN make all install JCC='python -m jcc' ANT=ant PYTHON=python NUM_FILES=8

# RUN rm -rf pylucene


######## LIBSEARCH ########

WORKDIR /home/libsearch

COPY . /home/libsearch

RUN pip install -e .

RUN cd /home/libsearch/ext/dexinfo && make && pip install -e .

CMD ["/bin/bash"]

RUN apt-get update \
    && apt-get install -y default-jdk ant



# ENTRYPOINT [ "python",  "-m", "unittest libsearch.tests.test_processing.TestProcessing.test_apk" ]

# CMD ["java", "Main"]