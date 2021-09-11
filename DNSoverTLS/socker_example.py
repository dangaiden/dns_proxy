import socket
import threading
import ssl
import dns.message
import dns.resolver
import dns.query
import binascii
SERVER='localhost'
PORT = 53000
ADDR = (SERVER, PORT)
DNS = "1.1.1.1"



def manage_request(addr, data, DNS, s):
    print (">>>>>>>>START Manage_request>>>>>>>>>>")
    print (f"|||ADDR:{addr}$$$${data}$$$${DNS}|||")
    print ("-----------------------")
    sock_tls=tls_connection(DNS) # FIRST, CREATE CONNECTION
    print (f"###Sock_tls connection:", sock_tls)
    tcp_answer = handle_query(sock_tls, data) 
    print (f"####AFTER HANDLE_QUERY Sock_tls:", sock_tls)
    print (f"||||///////Socket:{s}////TCP_ANSWER:{tcp_answer}////////ADDR:{addr}||||")
    #dns.query.send_udp(s, tcp_answer, addr))
    s.sendto(tcp_answer,addr) # Send back to client.
    print ("<<<<<<<<END Manage_request<<<<<<<<<")
#    if tcp_result

def tls_connection (DNS):  # Establishes a TCP connection with Upstream DNS
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Generate TCP socket.
    tcp_sock.settimeout(10)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)  # Needed SSLContext to handle certificates
    context.verify_mode = ssl.CERT_REQUIRED  # We enforce to have a certificate 
    context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
    wrapped_socket = context.wrap_socket(tcp_sock, server_hostname=DNS)
    wrapped_socket.connect((DNS , 853))
    print(wrapped_socket.getpeercert())  # PRINT remote cert details
    print ("_____________WRAPPED_DOCKET_PRINT_____________")
    print ((wrapped_socket))  # <ssl.SSLSocket object at 0x7f9649a49b50>
    
    return wrapped_socket

def handle_query (tls_sock, dns_query):
    print (">>>>START>>>>>Handle query FUNC")
    print (">>DNSQUERY:TYPE:",type(dns_query))
    #tcp_query=convert_query(dns)
    #tcp_query = binascii.unhexlify(dns_query)
    tcp_query = dns.message.from_wire(dns_query) #  GATHERING RAW QUERY and convert to DNS object
    tcp_query = dns.query.tls(tcp_query, "1.1.1.1", sock=tls_sock)
    print ("##TCP query SENT (FROM WIRE):", tcp_query)
    print ("11111TCP_QUERY OBJECT:", type(tcp_query))
    print ("------------")
    output = tcp_query.to_wire() # CONVERTING IT AGAIN TO RAW QUERY
    print ("------------")
    print ("@@@@@@@@@TCP query CONVERTED(TEXT):", tcp_query)
    print ("2222TCP_QUERY OBJECT:", type(tcp_query))
    #tcp_query = dns.query.receive_tcp (tls_sock)
    #print ("$$---TCP query RECEIVED:", tcp_query)
    #output = dns.query.send_tcp(tls_sock, tcp_query)
    #output = dns.query.tcp(tcp_query, tls_sock, timeout=10, port=853)
    #tls_sock.send(tcp_query)
    #output = tls_sock.recv(1024)
    print ("####Output from query (reply):", output)
    print ("####Output OBJECT:", type(output))
    print ("<<<END<<<<<<<Handle query FUNC<<<<<<<")
    return output

#def convert_query (socket): 
#    msg= dns.query.receive_udp (socket)



######################INIT#######################
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
        t = threading.Thread(target=manage_request, args=(addr, msg, DNS, s))
        t.start()
        print (f"Starting thread with [Address]:{addr} and [data]:{msg}")
except Exception as e:
    print (e)
finally:
    s.close()
##################END__INIT######################