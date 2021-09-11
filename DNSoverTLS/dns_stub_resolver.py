import socket
import os
import threading
import ssl
import dns.message
import dns.query

SERVER= os.environ['DNS_PROXY_IP'] #  IP address of DNS proxy
PORT = 53 #  Port of DNS proxy
ADDR = (SERVER, PORT)
DNS_SRV = "1.1.1.1" # One of Cloudflare's upstream servers.

def manage_request(addr, data, DNS, s): # Calls other functions with the incoming data from the client and sends it back.
    print (f"|||ADDR:{addr}$$$${data}$$$${DNS}|||")
    print ("-----------------------")
    sock_tls=tls_connection(DNS) #  First, we create a connection with Cloudflare in another function.
    print (f"###Sock_tls connection:", sock_tls)
    tcp_answer = handle_query(sock_tls, data) # We invoke another function and pass raw data and the socket created with Cloudflare.
    print (f"||||///////Socket:{s}////TCP_ANSWER:{tcp_answer}////////ADDR:{addr}||||")
    s.sendto(tcp_answer,addr) # Send back the response to the client.

def tls_connection (DNS):  # Establishes a TCP connection with Upstream DNS
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Generate TCP socket.
    tcp_sock.settimeout(10)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)  # Needed SSLContext to handle certificates
    context.verify_mode = ssl.CERT_REQUIRED  # We enforce to have a certificate .
    context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
    wrapped_socket = context.wrap_socket(tcp_sock, server_hostname=DNS)
    wrapped_socket.connect((DNS , 853))
    print ("_____________START_CERT__DETAILS____________")
    print(wrapped_socket.getpeercert())  # Print remote certificate details
    print ("_____________END_CERT__DETAILS____________")
    print ("[Wrapped Socket details created]:",(wrapped_socket))
    
    return wrapped_socket

def handle_query (tls_sock, dns_query):
    print (">>>>START>>>>>Handle query FUNC")
    print (">>DNSQUERY:TYPE:",type(dns_query))
    #tcp_query=convert_query(dns)
    #tcp_query = binascii.unhexlify(dns_query)
    tcp_query = dns.message.from_wire(dns_query) #  We gather the binary data and convert it to a dns.message obj to be handled later.
    tcp_query = dns.query.tls(tcp_query, "1.1.1.1", sock=tls_sock) # The module dns.query handles the send and receive of the DNS query.
    print ("##TCP query SENT (FROM WIRE):", tcp_query)
    print ("11111TCP_QUERY OBJECT:", type(tcp_query))
    print ("------------")
    output = tcp_query.to_wire() #  We convert it back from a dns.message object to a binary data response
    print ("------------")
    print ("@@@@@@@@@TCP query CONVERTED(TEXT):", tcp_query)
    print ("2222TCP_QUERY OBJECT:", type(tcp_query))
    print ("####Output from query (reply):", output)
    print ("####Output OBJECT:", type(output))
    print ("<<<END<<<<<<<Handle query FUNC<<<<<<<")
    return output

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #THIS IS UDP (SOCK_DGRAM)
    s.bind (ADDR)
    print ("Server socket created:", ADDR)
    while True:
        msg, addr = s.recvfrom(1024)
        print ("Connected from address:", addr)
        #msg = msg.decode(encoding="ascii")
        print ("Raw Data Received:", msg)
        print (type(msg))
        t = threading.Thread(target=manage_request, args=(addr, msg, DNS_SRV, s))
        t.start()
        print (f"Starting thread with [Address]:{addr} and [data]:{msg}")
except Exception as e:
    print (e)
finally:
    s.close()