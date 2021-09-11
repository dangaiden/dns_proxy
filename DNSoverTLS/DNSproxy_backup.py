import socket
import ssl
import sys
import thread
# import threading      
import binascii

#-----Add Length to query datagram
# convert the UDP DNS query to the TCP DNS query
def dnsquery(dns_query):
  pre_length = "\x00"+chr(len(dns_query)) #\x00,,,""
  _query = pre_length + dns_query
  print ("///////////////PRE_LENGTH///////////////////////////")
  print ((pre_length).encode("hex"))
  print ("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
  print ("///////////////DNS_QUERY///////////////////////////")
  print ((dns_query).encode("hex"))
  print ("+++++++++++++++++++++++++++++++++++++++++++++++++++")
  print ("//////////////////FULL_QUERY//////////////////////")
  print ((_query).encode("hex"))
  print ("++++++++++++++++++++++++++++++++++++++++++++++++++++")
  return _query

# send a TCP DNS query to the upstream DNS server
#-----Send Qquery to cloudfare server to get result
#<ssl.SSLSocket object at 0x7ff220192450>,:itgaidencom
def sendquery(tls_conn_sock,dns_query):
  tcp_query=dnsquery(dns_query) ##\x00+dns_query
  tls_conn_sock.send(tcp_query)
  result=tls_conn_sock.recv(1024) ## 1024 bytes ?  512 bytes is the limit for a DNS message
  print ("----------------------------------------")
  print ("----[TCP_QUERY]:-----")
  print ((tcp_query))
  print ("----------------------------------------")
  print ("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") 
  print ("----------------------------------------")
  print ("----[RESULT]:-----")
  print ((result))
  print ("----------------------------------------")
  return result

# a new thread to handle the UPD DNS request to TCP DNS request  
#------TLS connection with cloudflare server 
# Coming from requesthandle function
def tcpconnection(DNS): #Passing the DNS, let's start.
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket type IPV4, TCP
  sock.settimeout(10)
  context = ssl.SSLContext(ssl.PROTOCOL_SSLv23) # Needed SSLContext to handle certificates
  context.verify_mode = ssl.CERT_REQUIRED # We enforce to have a certificate 
  context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
  wrappedSocket = context.wrap_socket(sock, server_hostname=DNS)
  wrappedSocket.connect((DNS , 853))
  print(wrappedSocket.getpeercert())
  print ("$$$$$$$$__BEGIN_TCP_CONNECTION___$$$$$$$$$$$")
  print ((wrappedSocket))
  print ("$$$$$$$$__END_WRAPPEDSOCKET___$$$$$$$$$$$")
  return wrappedSocket

##########################################
#------ handle requests
def requesthandle(data,address,DNS):
   print ("Request from client: ", data.encode("hex"), addr)
   tls_conn_sock=tcpconnection(DNS) ## Before, let's create a tunnel with the upstream DNS
   tcp_result = sendquery(tls_conn_sock, data)
   print ("************TCP_RESULT**********************************")
   print ("TCP Answer from server: ", tcp_result.encode("hex"))
   #'00a3d0d78180000100010001000004636861740d737461636b6f766572666c6f7703636f6d00001c0001c00c000500010000010c001504636861740d737461636b65786368616e6765c01fc039000600010000010c004e0b6e732d636c6f75642d
   # 64310d676f6f676c65646f6d61696e73c01f14636c6f75642d646e732d686f73746d617374657206676f6f676c65c01f000000010000546000000e100003f4800000012c'
   print ("***********END_TCP_RESULT*************************")
   if tcp_result:
      rcode = tcp_result[:6].encode("hex")
      print ("--BEGIN-----tcp_result[:6].----------")
      print (rcode) # 0059ecca8180
      print ("--END----tcp_result[:6].----------")
      rcode = str(rcode)[11:] 
      print ("*************BEGIN-RCODE in string*********************")
      print ((rcode))# 0
      print ("*************END-RCODE in string****************************")
      if (int(rcode, 16) ==1): # QR              A one bit field that specifies whether this message is a query (0), or a response (1).
         print ("not a dns query")
      else:
         udp_result = tcp_result[2:]
         s.sendto(udp_result,address)
         print ("**********************************************")
         print ("200")
         print ("***************200-RCODE******************")
         print ((rcode).encode("hex"))
         print ("--TCP_RESULT--")
         print ((tcp_result).encode("hex"))
         print ("ooooooooooooooooooooooooooooooooooooooooooooooooo")
         print ("HHHHHHHHHHHHHH***UDP_RESULT****HHHHHHHHHHHHHHHHHHH")
         print ((udp_result).encode("hex"))
         print ("--ADDRESS--")
         print ((address))
         print ("**********************************************")
         print ("tcpresult!")
         print ("77777777777777777777777777777777777777777777777777777777777777777")
   else:
      print ("not a dns query")
      print ("33333333333333333333333333333333333333333333333333333333333333333")

###Execution
if __name__ == '__main__': ## Only executed when this is the main program
   DNS = '1.1.1.1'
   port = 53
   host='172.168.1.2'
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #THIS IS UDP (SOCK_DGRAM)
      s.bind((host, port))
      while True:
        data,addr = s.recvfrom(1024)
        thread.start_new_thread(requesthandle,(data, addr, DNS))
        print ("8888888***************888888888888888****************888888888")
        print ((data))
        print ((addr))
        print ((DNS))
        print ("8888888***************888888888888888****************888888888")
   except Exception, e:
      print (e)
      s.close()



# TCP uses SOCK_STREAM and UDP uses SOCK_DGRAM.