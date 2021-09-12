# README 

## DNS-proxy project

### Summary

This project aims to provide the functionality of a DNS proxy over TLS.
It aims to be used as a micro-service (within a container) so you can specify an IP address (called using -e when running the container with Docker) that will listen on port 53, therefore, DNS requests sent to that IP address will be handled by the DNS proxy.

The proxy reads the query sent via UDP, creates an encrypted connection with an upstream server (Cloudflare) over TCP(TLS) and handles back the response to the client.

It requires the [dnspython](https://www.dnspython.org/) library, as it will handle all the binary data from the requests and replies, otherwise, you will have to manage the raw data from the client and the upstream server.
### Running the project in a container

- Create a network to avoid problems within your own LAN. Therefore
you should create a new docker network by executing (or use one you already have):

```
docker network create --subnet 192.168.10.0/24 dns_network
```

- Proceed to create the docker image by using the Dockerfile provided by running:
```
docker build -t <your-image-name> .
```
Example:
```
docker build -t dns_srv_proxy .
```

- Run the container in dettached mode within the docker network created previously:

```
docker run --name <your-container-name> -e DNS_PROXY_IP=<IP-address> -d --net <your-docker-network> <your-image-name>
```

Example:
```
docker run --name proxy_dns -e DNS_PROXY_IP=192.168.10.2 -d --net dns_network dns_srv_proxy
```

- To test it you can do it in different ways:

You can try to use the IP address of the DNS proxy as your DNS/Nameserver and perform a nslookup or just navigate using your web browser.

Tested it with the following tools: nslookup and dig

Some examples:

``` # Using dig
dig @192.168.10.2 -p 53 www.preply.com

; <<>> DiG 9.11.5-P4-5.1+deb10u5-Debian <<>> @192.168.10.2 -p 53 www.preply.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 59750
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; PAD: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 (".....................................................................................................................................................................................................................................................................................................................................................................................................")
;; QUESTION SECTION:
;www.preply.com.			IN	A

;; ANSWER SECTION:
www.preply.com.		300	IN	A	104.18.20.180
www.preply.com.		300	IN	A	104.18.21.180

;; Query time: 127 msec
;; SERVER: 192.168.10.2#53(192.168.10.2)
;; WHEN: Sat Sep 11 19:07:25 CEST 2021
;; MSG SIZE  rcvd: 468
```
---
``` # Using the DNS proxy as my nameserver (Replace all the content with "nameserver 192.168.10.2" in your etc/resolv.conf file, or change it from the NIC properties on Windows and MAC.)

nslookup www.bcc.com
Server:		192.168.10.2
Address:	192.168.10.2#53

Non-authoritative answer:
www.bcc.com	canonical name = bcc.com.
Name:	bcc.com
Address: 184.168.221.96

```

## Possible improvements

- Control error of messages (RCODE for example)
- Add TCP connectivity between client and proxy.
- Add caching to gain performance in repetitive queries.
# References used for this project

- https://docs.python.org/3/library/ssl.html
- https://docs.python.org/3.7/library/socket.html
- https://pythontic.com/ssl/sslcontext/wrap_socket
- https://datatracker.ietf.org/doc/html/rfc1035
- https://routley.io/posts/hand-writing-dns-messages/
- https://gist.github.com/mrpapercut/92422ecf06b5ab8e64e502da5e33b9f7#file-raw-dns-req-py-L15
- https://github.com/tigerlyb/DNS-Proxy-Server-in-Python/blob/master/DNSProxyServer.py
- https://developers.cloudflare.com/1.1.1.1/encrypted-dns/dns-over-tls


