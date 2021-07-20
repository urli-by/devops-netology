FROM centos:7
EXPOSE 9200 9300
COPY --chown=root:root elasticsearch.repo /etc/yum.repos.d/
RUN rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
RUN yum upgrade -y && yum install --enablerepo=elasticsearch -y elasticsearch
COPY --chown=root:elasticsearch elasticsearch.yml /etc/elasticsearch/
RUN mkdir /var/lib/elasticsearch/snapshots && chown elasticsearch:elasticsearch /var/lib/elasticsearch/snapshots
USER elasticsearch
ENTRYPOINT [ "/usr/share/elasticsearch/bin/elasticsearch" ]