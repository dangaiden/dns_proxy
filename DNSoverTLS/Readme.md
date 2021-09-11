# README 

## DNS-proxy project

### Summary

This will create a container with a DNS proxy function.
It has a pre-defined IP address (within the python code) that will listen on port 53, therefore, DNS requests sent to that IP address will be handled by the DNS proxy.

The proxy reads the query sent via UDP, creates a connection with an upstream server (Cloudflare) over TCP(TLS) and handles back the response to the client.

### Running the project

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
docker run --name proxy_dns -e DNS_PROXY_IP=192.168.10.2 -d --net dns_nw10 dns_srv_proxy
```

- To test it you can do it in different ways:

You can try to use the IP address of the DNS proxy as your DNS/Nameserver and perform a nslookup or just navigate using web browser.

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


## Improvements

- Add TCP connectivity between client and proxy.
- Buffer/Cache
- SSL offloading

## Question

We are also asking you to describe how you will deploy the proxy in a cloud-based infrastructure with various client applications already deployed in it. (Just a text description. You can also attach a
scheme/diagram if it makes sense, no strong requirements here).

### Answer

Regarding the proxy, the best scenario will be within the same network (LAN) where different applications are located.

This means that if we have different environments, as they will be in different networks, a proxy for each enviroment will be the best fit to process all the requests from the different applications and to provide security.

The packets between the proxy and the upstream DNS server are sent over an encrypted connection so there is no expected security risks.

In the other hand, in my case where the proxy doesn't support TCP from the client side (LAN), it would be mandatory to do it within the internal network.

As the connection won't be encrypted **between the proxy and the clients (applications)**, it will be vulnerable to a Man-in-the-middle (MITM) attacks as the DNS queries are sent over the plain text connection.

# References

https://docs.python.org/3/library/ssl.html
https://docs.python.org/3.7/library/socket.html
https://datatracker.ietf.org/doc/html/rfc1035
https://routley.io/posts/hand-writing-dns-messages/
https://gist.github.com/mrpapercut/92422ecf06b5ab8e64e502da5e33b9f7#file-raw-dns-req-py-L15
https://github.com/tigerlyb/DNS-Proxy-Server-in-Python/blob/master/DNSProxyServer.py


