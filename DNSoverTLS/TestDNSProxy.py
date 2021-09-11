import socket
import ssl
import sys
import threading
# import threading      
# import binascii

#-----Add Length to query datagram
def dnsquery(dns_query):
  pre_length = "\x00"+chr(len(dns_query))
  _query = pre_length + dns_query
  return _query

#-----Send Qquery to cloudfare server to get result
def sendquery(tls_conn_sock,dns_query):
  tcp_query=dnsquery(dns_query)
  tls_conn_sock.send(tcp_query)
  result=tls_conn_sock.recv(1024) ## 1024 bytes ?  512 bytes is the limit for a DNS message
  return result

  
#------TLS connection with cloudflare server  
def tcpconnection(DNS):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(10)
  context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  context.verify_mode = ssl.CERT_REQUIRED
  context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
  wrappedSocket = context.wrap_socket(sock, server_hostname=DNS)
  wrappedSocket.connect((DNS , 853))
  print(wrappedSocket.getpeercert())
  return wrappedSocket

##########################################
#------ handle requests
def requesthandle(data,address,DNS):
    tls_conn_sock=tcpconnection(DNS) 
    tcp_result = sendquery(tls_conn_sock, data)
    print (f"[BEFORE ENTERING IF - TCP_RESULT]:{tcp_result}!")
    if tcp_result:
        rcode = tcp_result[:6].encode("hex") # Print from the beggining of the string until the 6th position.
        rcode = str(rcode)[11:]#Print from 11th position until the end of the string.
        if (int(rcode, 16) ==1):
            print ("not a dns query")
            print ("###################")
        else:
            udp_result = tcp_result[2:]
            s.sendto(udp_result,address)
            print ("200")
            print (f"**********************")
            print (f"[AFTER ENTERING IF - RCODE]:{rcode}")
            print (f"[AFTER ENTERING IF - TCP_RESULT]:{tcp_result}!")
            print (f"[AFTER ENTERING IF - UDP_RESULT]:{udp_result}!")

    print ("tcpresult!")
#     print (f"[RCODE]={rcode}")
#     print (f"**********************")
    print (f"[AFTER ENTERING 1st IF - TCP_RESULT]{tcp_result}!")
    else:
        print ("not a dns query")

###Execution
if __name__ == '__main__': ## Only executed when this is the main program
   DNS = '1.1.1.1'
   port = 33333
   host='192.168.1.229'
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #THIS IS UDP (SOCK_DGRAM)
   s.bind((host, port))
   while True:
    data,addr = s.recvfrom(1024)
    threading.Thread(requesthandle,(data, addr, DNS))
   s.close()

# TCP uses SOCK_STREAM and UDP uses SOCK_DGRAM.