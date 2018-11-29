FROM python:2.7

WORKDIR /home/libsearch
COPY setup.py /home/libsearch
# ENTRYPOINT [ "/bin/bash" ]
RUN "pip install -e ."

CMD ["/bin/bash"]
# ENTRYPOINT [ "python",  "-m", "unittest libsearch.tests.test_processing.TestProcessing.test_apk" ]

# CMD ["java", "Main"]