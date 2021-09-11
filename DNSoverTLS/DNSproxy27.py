import socket
import ssl
import sys
import thread
# import threading      
import binascii

#-----Add Length to query datagram
def dnsquery(dns_query):
  print ("///////////DNS_QUERY/////////")
  print (dns_query)
  print (type(dns_query))
  pre_length = "\x00"+chr(len(dns_query)) #\x00,,,""
  _query = pre_length + dns_query
  print ("|||||||||PRELENGTH||||||||||||")
  print (pre_length.encode("hex"))
  print ("///////////_QUERY/////////")
  print (_query)
  print (type(_query))
  print ("____END_________DNSQUERY___FUNCTION__________")
  return _query

#-----Send Qquery to cloudfare server to get result
def sendquery(tls_conn_sock,dns_query):
  print ("########<<<<PRINT_DNS_QUERY<<<<#######")
  print(dns_query) # ghosterycom
  tcp_query=dnsquery(dns_query) ##\x00+dns_query (CONVERT)
  print ("<<<<PRINT_TCP_QUERY<<<<<<<<<<<<<<<<<<<<")
  print(tcp_query) # ghosterycom
  tls_conn_sock.send(tcp_query)
  result=tls_conn_sock.recv(1024) ## 1024 bytes ?  512 bytes is the limit for a DNS message
  print ("BEFORE TUNINGREEEEEEEEESUUUUUULTTT")
  print (type(result))
  #result = bytes.decode(result) # Convert to string
  print ("--******--[RESULT]:--****---")
  print (result)
  print ("____END_________SEND_QUERY___FUNCTION__________")

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
  print ("_____________BEGIN_TCP_CONNECTION_____________")
  print ((wrappedSocket)) # <ssl.SSLSocket object at 0x7f9649a49b50>
  print ("$$$$$$$$__END_WRAPPEDSOCKET___$$$$$$$$$$$")
  return wrappedSocket

##########################################
#------ handle requests
def requesthandle(data,address,DNS):
   print ("=======================REQUEST===HANDLE====================")
   print ("Request from client: ", data, addr)
   tls_conn_sock=tcpconnection(DNS)
   print (">>>>>>>>MOVING TO TCP_RESULT__LINE71 (SENDQUERY FUNCTION)>>>>>>>>>>>>DATA:")
   print ("[DATA]: ",data)
   print ("[TLS_CONN_SOCK]: ",tls_conn_sock)
   tcp_result = sendquery(tls_conn_sock, data)
   print ("************TCP_RESULT***ANSWER FROM SERVER & DATA*******************************")
   print (tcp_result.encode("hex"))
   print ("=======================END_TCP_RESULT=======================")
   if tcp_result:
      rcode = tcp_result[:6].encode("hex")
      print (">>>RCODE:6->>", rcode)
      print ("<<<RCODE:6->TYPE<", type(rcode))
      rcode = str(rcode)[11:]
      print (">>>RCODE11:->>", rcode)
      print ("<<<RCODE11:-<<", type(rcode))
      if (int(rcode, 16) ==1):
         print ("not a dns query")
      else:
         udp_result = tcp_result[2:]
         s.sendto(udp_result,address)
         print ("**********************************************")
         print ("200")
         print ("-RECEIVED-TCP_RESULT--")
         print (tcp_result)#00405ec8818000010002000000000377777706707265706c7903636f6d0000010001c00c000100010000012c0004681214b4c00c000100010000012c0004681215b4
         print ("ooooooooooooooooooooooooooooooooooooooooooooooooo")
         print ("@@@@@@@@@@@@@***UDP_RESULT****HHHHHHHHHHHHHHHHHHH")
         print (udp_result) #5ec8818000010002000000000377777706707265706c7903636f6d0000010001c00c000100010000012c0004681214b4c00c000100010000012c0004681215b4
         print ("--ADDRESS--")
         print (address) # ('172.168.1.1', 54461)
         print ("**********************************************")
         print ("tcpresult!")
         print ("77777777777777777777777777777777777777777777777777777777777777777")
   else:
      print ("not a dns query")
      print ("OOOOOOOOOOUUUUUUUUUUUUUUUTTTTTT")

###Execution
if __name__ == '__main__': ## Only executed when this is the main program
   DNS = '1.1.1.1'
   PORT = 53000
   HOST ='localhost'
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #THIS IS UDP (SOCK_DGRAM)
      s.bind((HOST, PORT))
      while True:
        data,addr = s.recvfrom(1024)
        thread.start_new_thread(requesthandle,(data, addr, DNS))
        print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>NEW THREAD WITH:<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print ("Data (NOT HEX) from the client: ",(data)) #\x9b\xc7\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06preply\x03com\x00\x00\x1c\x00\x01
        print ("Address of sender: ",(addr)) # 172.168.1.1', 52533
        print ((DNS))
        print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
   except Exception, e:
      print (e)
      s.close()


# TCP uses SOCK_STREAM and UDP uses SOCK_DGRAM.