import socket
import ssl
import sys
import thread
# import threading      
import binascii



#-----Add Length to query datagram
# convert the UDP DNS query to the TCP DNS query
# dns_query/data -> 9bc7010000010000000000000377777706707265706c7903636f6d00001c0001
def dnsquery(dns_query):
  pre_length = "\x00"+chr(len(dns_query)) #0020 Prelength (hex), len(dns_query)=y", chr(len(dns_query)=64, @=prelength or 0040 (hex)
  _query = pre_length + dns_query
  print ("///////////////PRE_LENGTH///////////////////////////")
  print ((pre_length).encode("hex"))
  print (type(dns_query)) #string
  print ("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
  print ("///////////////DNS_QUERY STRING///////////////////////////")
  print (dns_query) # wwwpreplycom
  print ("///////////////DNS_QUERY HEX///////////////////////////")
  print ((dns_query).encode("hex")) #9bc7010000010000000000000377777706707265706c7903636f6d00001c0001
  print ("+++++++++++++++++++++++++++++++++++++++++++++++++++")
  print ("//////////////////FULL_QUERY//////////////////////")
  print ((_query).encode("hex")) # 00209bc7010000010000000000000377777706707265706c7903636f6d00001c0001
  print ("++++++++++++++++++++++++++++++++++++++++++++++++++++")
  return _query

# send a TCP DNS query to the upstream DNS server
#-----Send Qquery to cloudfare server to get result
#<ssl.SSLSocket object at 0x7ff220192450>,:itgaidencom
def sendquery(tls_conn_sock,dns_query):
  tcp_query=dnsquery(dns_query) ##\x00+dns_query
  tls_conn_sock.send(tcp_query) # Send tuned query.
  result=tls_conn_sock.recv(1024) ## 1024 bytes ?  512 bytes is the limit for a DNS message
  print ("----------------------------------------")
  print ("----[TCP_QUERY]:-----")
  print ((tcp_query))
  print ("----------------------------------------")
  print ("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") 
  print ("----------------------------------------")
  print ("----[RESULT]:-----")
  print ((result)) #
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
  print(wrappedSocket.getpeercert()) # PRINT remote cert details
  print ("_____________BEGIN_TCP_CONNECTION_____________")
  print ((wrappedSocket)) # <ssl.SSLSocket object at 0x7f9649a49b50>
  print ("$$$$$$$$__END_WRAPPEDSOCKET___$$$$$$$$$$$")
  return wrappedSocket

##########################################
#------ handle requests
def requesthandle(data,address,DNS):
   print ("=======================REQUEST===HANDLE====================")
   print ("Request from client: ", data, addr)
   tls_conn_sock=tcpconnection(DNS) ## Before continuing, let's create a tunnel with the upstream DNS
   tcp_result = sendquery(tls_conn_sock, data) #Answer from server after tuning and sending the query.
   print ("************TCP_RESULT**********************************")
   print ("TCP Answer from server: ", tcp_result.encode("hex"))
   #'00405ec8818000010002000000000377777706707265706c7903636f6d0000010001c00c000100010000012c0004681214b4c00c000100010000012c0004681215b4'
   print ("=======================END_TCP_RESULT=======================")
   if tcp_result: # Checking if tcp_result has content (not equal to 0 or None)
      rcode = tcp_result[:6].encode("hex")
      print ("--BEGIN-----tcp_result[:6].----------")
      print (type(tcp_result))
      print (tcp_result[:6]) #
      print ("--END----tcp_result[:6].----------")
      print ("*************BEGIN-RCODE in HEX*********************")
      print (rcode) # 00 40 5e c8 81 80
      print ("*************END-RCODE in HEX*********************")
      rcode = str(rcode)[11:] # Pick last Bit
      print ("*************BEGIN-RCODE in string*********************")
      print ((rcode))# 0
      print ("=======================END-RCODE in string=======================")
      if (int(rcode, 16) ==1): # QR  A one bit field that specifies whether this message is a query (0), or a response (1).
         print ("not a dns query") #Meaning it's a reply with content () different than "000000000...1".
      else:
         udp_result = tcp_result[2:] 
         s.sendto(udp_result,address)
         print ("**********************************************")
         print ("200")
         print ("--TCP_RESULT--")
         print ((tcp_result).encode("hex"))#00405ec8818000010002000000000377777706707265706c7903636f6d0000010001c00c000100010000012c0004681214b4c00c000100010000012c0004681215b4
         print ("ooooooooooooooooooooooooooooooooooooooooooooooooo")
         print ("HHHHHHHHHHHHHH***UDP_RESULT****HHHHHHHHHHHHHHHHHHH")
         print ((udp_result).encode("hex")) #5ec8818000010002000000000377777706707265706c7903636f6d0000010001c00c000100010000012c0004681214b4c00c000100010000012c0004681215b4
         print ("--ADDRESS--")
         print ((address)) # ('172.168.1.1', 54461)
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
      print ("---------------------BEFORE while True:---------------------------")
      while True:
        data,addr = s.recvfrom(1024)
        thread.start_new_thread(requesthandle,(data, addr, DNS))
        print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>NEW THREAD WITH:<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print ("Data (NOT HEX) to be sent to the proxy: ",(data)) #\x9b\xc7\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06preply\x03com\x00\x00\x1c\x00\x01
        print ("Data (HEX) to be sent to the proxy: ", data.encode("hex"))# 9bc7010000010000000000000377777706707265706c7903636f6d00001c0001
        print ("Address of sender: ",(addr)) # 172.168.1.1', 52533
        print ((DNS))
        print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
   except Exception, e:
      print (e)
      s.close()



# TCP uses SOCK_STREAM and UDP uses SOCK_DGRAM.