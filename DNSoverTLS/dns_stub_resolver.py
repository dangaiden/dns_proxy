import socket
import os
import threading
import ssl
import dns.message
import dns.query

# Constants variables

SERVER = "localhost" #  IP address of DNS proxy
PORT = 53000 #  Port of DNS proxy
ADDR = (SERVER, PORT)
DNS_SRV = "one.one.one.one" # One of Cloudflare's upstream servers.

def manage_request(addr, data, DNS, s): # Calls other functions with the incoming data from the client and sends it back.
    sock_tls=tls_connection(DNS) #  First, we create a connection with Cloudflare in another function.
    print (f"### [TLS CONNECTION SOCKET CREATED]:{sock_tls}###")
    tls_answer = handle_query(sock_tls, data, DNS) #  We invoke another function to send raw data and the previous socket created with Cloudflare.
    print (f"$$$ [TLS_ANSWER]:{tls_answer}")
    print (f"$$$ [CLIENT ADDRESS]:{addr}")
    s.sendto(tls_answer,addr) #  Send back the response to the client.

def tls_connection (DNS):  
    #  Establishes a TCP connection with Upstream DNS. Then creates an SSL connection by wrapping the socket.
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #  Generate TCP socket.
    tcp_sock.settimeout(10)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)  # Select highest protocol version (auto-negotiated)
    context.verify_mode = ssl.CERT_REQUIRED  #  We enforce to have a certificate .
    context.load_verify_locations("/etc/ssl/certs/ca-certificates.crt") #  Load a CA certificate that will be used to validate the certificate from the server.
    wrapped_socket = context.wrap_socket(tcp_sock, server_hostname=DNS) #  Wrap socket using the previous context and DNS.
    wrapped_socket.getpeername()
    wrapped_socket.connect(DNS , 853) #  Connect to Upstream DNS (Cloudflare)
    print ("[Wrapped Socket Peer Name]:",(wrapped_socket.getpeername()))
    print ("_____________START_CERT__DETAILS____________")
    print(wrapped_socket.getpeercert())  #  Print remote certificate details
    print ("_____________END_CERT__DETAILS____________")
    print ("[Wrapped socket details created]:",(wrapped_socket))
    
    return wrapped_socket

def handle_query (tls_sock, dns_query, DNS):
    tcp_query = dns.message.from_wire(dns_query) #  We gather the binary data and convert it to a dns.message obj to be handled later.
    tcp_query = dns.query.tls(tcp_query, DNS, sock=tls_sock) # The module dns.query handles the send and receive of the DNS query.
    print ("### TCP query SENT ", tcp_query)
    print ("------------")
    output = tcp_query.to_wire() #  We convert it back from a dns.message object to a binary data response
    print ("------------")
    print ("### [Output from Handle_query (Answer from Cloudflare)]:",output)
    
    return output

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #  Defined UDP socket
    s.bind (ADDR)
    print ("Server socket created, listening on:", ADDR)
    while True: # Infinite loop until there is no more data or we explictly break it.
        msg, addr = s.recvfrom(1024) 
        # Create thread for each packet that we receive from a client.
        t = threading.Thread(target=manage_request, args=(addr, msg, DNS_SRV, s))
        t.start()
        print (f"Starting thread with [Address]:{addr} and [data]:{msg}")
except Exception as e:
    print (e)
finally:
    s.close()