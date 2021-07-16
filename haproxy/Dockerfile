FROM haproxy:2.4

WORKDIR /workdir

# We need to be root for the next bit
USER root

RUN apt-get update && apt-get install -y ca-certificates openssl && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/haproxy/ssl
# Based on https://gist.github.com/yuezhu/47b15b4b8e944221861ccf7d7f5868f5
RUN openssl genrsa -out /etc/haproxy/ssl/server.key 2048 && \
    openssl req -new -key /etc/haproxy/ssl/server.key -out /etc/haproxy/ssl/server.csr \
      -subj "/C=US/ST=Oregon/L=Portland/O=OrgName/OU=haproxy-logging-and-metrics/CN=haproxy.xormedia.com" && \
    openssl x509 -req -days 365 -in /etc/haproxy/ssl/server.csr -signkey /etc/haproxy/ssl/server.key -out /etc/haproxy/ssl/server.crt && \
    cat /etc/haproxy/ssl/server.key /etc/haproxy/ssl/server.crt >> /etc/haproxy/ssl/server.pem

COPY etc/ /etc

# We can go back to being haproxy now
USER haproxy

CMD /usr/local/sbin/haproxy -C /etc/haproxy -f /etc/haproxy/haproxy.cfg
