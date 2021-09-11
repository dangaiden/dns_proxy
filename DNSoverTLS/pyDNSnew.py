import socket
import threading
import ssl
import dns.query

SERVER='localhost'
PORT = 53000
ADDR = (SERVER, PORT)
DNS = "1.1.1.1"



def manage_request(addr, data, DNS):
    print (">>>>>>>>START Manage_request>>>>>>>>>>")
    print (addr, data, DNS)
    print ("-----------------------")
    sock_tls=tls_connection(DNS)
    print (f"###Sock_tls connection:", sock_tls)
    tcp_answer = send_query(sock_tls, data)
    print (f"Before tune -Sock_tls:", sock_tls)
    tcp_answer = dns.query.receive_tcp(sock_tls)
    print (f"After tune -Sock_tls:", sock_tls)
    s.sendto(tcp_answer,addr) # Send back to client.
    print ("<<<<<<<<END Manage_request<<<<<<<<<")
#    if tcp_result

def tls_connection (DNS):  # Establishes a TCP connection with Upstream DNS
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Generate TCP socket.
    tcp_sock.settimeout(5)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS) # Needed SSLContext to handle certificates
    context.verify_mode = ssl.CERT_REQUIRED # We enforce to have a certificate 
    context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
    wrapped_Socket = context.wrap_socket(tcp_sock, server_hostname=DNS)
    wrapped_Socket.connect((DNS , 853))
    print(wrapped_Socket.getpeercert()) # PRINT remote cert details
    print ("_____________WRAPPED_DOCKET_PRINT_____________")
    print ((wrapped_Socket)) # <ssl.SSLSocket object at 0x7f9649a49b50>
    
    return wrapped_Socket

def send_query (tls_sock, dns_query):
    print (">>>>START>>>>>Send query FUNC")
    tcp_query = convert_query(dns_query)
    print ("##TCP query:", tcp_query)
    #tls_sock.send(tcp_query)
    #output = dns.query.receive_tcp(tls_sock)
    #print ("####Output from query (reply):", output)
    print ("<<<END<<<<<<<Send query FUNC<<<<<<<")
    #return output
    return tcp_query

def convert_query (socket): 
    msg= dns.query.receive_udp (socket)



######################INIT#######################
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #THIS IS UDP (SOCK_DGRAM)
    s.bind (ADDR)
    print ("Server socket created:", ADDR)
    while True:
        msg, addr = s.recvfrom(1024)
        print ("Connected from address:", addr)
        print ("Data:", msg)
        t = threading.Thread(target=manage_request, args=(addr, msg, DNS,))
        t.start()
        print (f"Starting thread with Address:{addr} and data:{msg}")
except Exception as e:
    print (e)
finally:
    s.close()
##################END__INIT######################