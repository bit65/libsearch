FROM python:2.7

WORKDIR /home/libsearch

COPY . /home/libsearch

RUN pip install -e .

RUN cd /home/libsearch/ext/dexinfo && make && pip install -e .

CMD ["/bin/bash"]
# ENTRYPOINT [ "python",  "-m", "unittest libsearch.tests.test_processing.TestProcessing.test_apk" ]

# CMD ["java", "Main"]