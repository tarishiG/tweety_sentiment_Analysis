# start with a base image
FROM ubuntu:18.04

MAINTAINER Real Python <info@realpython.com>

# initial update
RUN apt-get update -y

# install wget, java, and mini-httpd web server
RUN apt-get install wget -y
RUN apt-get install default-jre-headless -y
RUN apt-get install mini-httpd -y

# install elasticsearch
RUN cd /tmp && \
    wget -nv https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-7.0.0.tar.gz && \
    tar zxf elasticsearch-7.0.0.tar.gz && \
    rm -f elasticsearch-7.0.0.tar.gz && \
    mv /tmp/elasticsearch-7.0.0 /elasticsearch

# install kibana
RUN cd /tmp && \
    wget -nv https://download.elasticsearch.org/kibana/kibana/kibana-3.1.2.tar.gz && \
    tar zxf kibana-7.0.0.tar.gz && \
    rm -f kibana-7.0.0.tar.gz && \
    mv /tmp/kibana-7.0.0 /kibana

# start elasticsearch
CMD /elasticsearch/bin/elasticsearch -Des.logger.level=OFF & mini-httpd -d /kibana -h `hostname` -r -D -p 8000

# expose ports
EXPOSE 8000 9200
