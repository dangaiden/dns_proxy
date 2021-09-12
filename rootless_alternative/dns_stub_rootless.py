import socket
import os
import threading
import ssl
import dns.message
import dns.query

# Rootless version which runs in a higher port than 5300.

# Constants variables
SERVER = os.environ.get("DNS_PROXY_IP") #  IP address of DNS proxy expected to be gathered from ENV variables (used in docker run -e <var>=<value>)
PORT = 5300 #  Port of DNS proxy
ADDR = (SERVER, PORT)
DNS_SRV = "1.1.1.1" #  One of Cloudflare's upstream servers. Used IP address as hostname "one.one.one.one" points to 1.0.0.1

def manage_request(addr, data, DNS, s): # Calls other functions with the incoming data from the client and sends it back.
    sock_tls=tls_connection(DNS) #  First, we create a connection with Cloudflare in another function.
    print (f"$$$ [TLS CONNECTION SOCKET CREATED]:{sock_tls} ###")
    tls_answer = handle_query(sock_tls, data, DNS) #  We invoke another function to send raw data and the previous socket created with Cloudflare.
    print (f"$$$ [RAW ANSWER FROM UPSTREAM DNS SERVER]:{tls_answer}###")
    s.sendto(tls_answer,addr) #  Send back the response to the client.
    print (f"$$$ RESPONSE WAS SUCCESSFULLY SENT TO: {addr}")

def tls_connection (DNS):  
    #  Establishes a TCP connection with Upstream DNS. Then creates an SSL connection by wrapping the socket.
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #  Generate TCP socket.
    tcp_sock.settimeout(10)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)  # Select highest protocol version (auto-negotiated)
    context.verify_mode = ssl.CERT_REQUIRED  #  We enforce to have a certificate .
    context.load_verify_locations("/etc/ssl/certs/ca-certificates.crt") #  Load a CA certificate that will be used to validate the certificate from the server.
    wrapped_socket = context.wrap_socket(tcp_sock, server_hostname=DNS) #  Wrap socket using the previous context and DNS.
    #wrapped_socket.getpeername()
    wrapped_socket.connect((DNS, 853)) #  Connect to Upstream DNS (Cloudflare)
    #print ("[Wrapped Socket Peer Name]:",(wrapped_socket.getpeername()))
    print ("_____________START_CERT__DETAILS____________")
    print(wrapped_socket.getpeercert())  #  Print remote certificate details
    print ("_____________END_CERT__DETAILS____________")
    print ("[Wrapped socket details created]:",(wrapped_socket))
    
    return wrapped_socket

def handle_query (tls_sock, dns_query, DNS):
    tcp_query = dns.message.from_wire(dns_query) #  We gather the binary data and convert it to a dns.message obj to be handled later.
    tcp_query = dns.query.tls(tcp_query, DNS, sock=tls_sock) # The module dns.query handles the send and receive of the DNS query.
    print ("$$$ [TCP RESPONSE RECEIVED]:", tcp_query)
    print ("------------")
    if tcp_query:
        output = tcp_query.to_wire() #  We convert it back from a dns.message object to a binary data response
        return output
    else:
        print (f"REPLY EMPTY: {tcp_query}")

if __name__ == "__main__": #  Boilerplate code to know if this module is being run directly and not imported.
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
    except KeyboardInterrupt:
        s.close()
        print ("Socket closed due to Keyboard Interrupt (CTRL+C)")
    except OSError as OS:
        print ("OS error:", OS)
    except Exception as e:
        print ("General error:", e)