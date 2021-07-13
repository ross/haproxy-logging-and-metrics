FROM haproxy:2.4

WORKDIR /workdir

COPY etc/ /etc

CMD /usr/local/sbin/haproxy -V -C /etc/haproxy -f /etc/haproxy/haproxy.cfg
