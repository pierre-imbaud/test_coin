# test coin dockerfile
FROM python:3.7.5

WORKDIR /usr/src/lib
COPY lib .

WORKDIR /usr/src/bin
COPY scripts/find_square .

WORKDIR /usr/src
COPY example_file .

ENV PYTHONPATH /usr/src/lib
ENV PATH $PATH:/usr/src/bin


RUN python -m pip install \
        ipython  
