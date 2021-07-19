FROM    centos:7

RUN 	groupadd -g 1000 elasticsearch && \
		adduser -u 1000 -g 1000 -G 0 -d /usr/share/elasticsearch elasticsearch && \
		chmod 0775 /usr/share/elasticsearch && \
		chown -R 1000:0 /usr/share/elasticsearch

RUN 	rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
RUN     yum update -y && yum install -y wget sudo perl-Digest-SHA; yum clean all
RUN		sudo yum -y install java-1.8.0-openjdk  java-1.8.0-openjdk-devel
RUN		wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.13.3-x86_64.rpm
RUN		wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.13.3-x86_64.rpm.sha512
RUN		shasum -a 512 -c elasticsearch-7.13.3-x86_64.rpm.sha512
RUN		sudo rpm --install elasticsearch-7.13.3-x86_64.rpm
RUN		yum update -y

WORKDIR /usr/share/elasticsearch
COPY 	elasticsearch.yml /usr/share/elasticsearch/config/
USER 	elasticsearch
ENV 	PATH=$PATH:/var/lib
CMD 	["elasticsearch"]
EXPOSE 	9200 9300