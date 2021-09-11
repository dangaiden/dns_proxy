import socket
import ssl
import sys
#import thread
import threading      
import binascii

#-----Add Length to query datagram
def dnsquery(dns_query):
  pre_length = "\x00"+chr(len(dns_query)) #\x00,,,""
  _query = pre_length + dns_query
  print ("///////////////////////////////////////////////////")
  print ((_query))
  print ("///////////////////////////////////////////////////")
  return _query

#-----Send Qquery to cloudfare server to get result
def sendquery(tls_conn_sock,dns_query):
  tcp_query=dnsquery(dns_query) ##\x00+dns_query
  tls_conn_sock.send(tcp_query)
  result=tls_conn_sock.recv(1024) ## 1024 bytes ?  512 bytes is the limit for a DNS message
  print ("----------------------------------------")
  print ("----[TCP_QUERY]:-----")
  print ((tcp_query))
  print ("----------------------------------------")
  print ("//////////////////////////////////////////////////") 
  print ("----------------------------------------")
  print ("----[RESULT]:-----")
  print ((result))
  print ("----------------------------------------")
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
  print ("$$$$$$$$__BEGIN_TCP_CONNECTION___$$$$$$$$$$$")
  print ((wrappedSocket))
  print ("$$$$$$$$__END_WRAPPEDSOCKET___$$$$$$$$$$$")
  return wrappedSocket
  

##########################################
#------ handle requests
def requesthandle(data,address,DNS):
   tls_conn_sock=tcpconnection(DNS) 
   tcp_result = sendquery(tls_conn_sock, data)
   print ("************TCP_RESULT**********************************")
   print ((tcp_result))
   print ("**********************************************")
   if tcp_result:
      rcode = tcp_result[:6].encode("hex")
      rcode = str(rcode)[11:]
      if (int(rcode, 16) ==1):
         print ("not a dns query")
         print ("###################")
      else:
         udp_result = tcp_result[2:]
         s.sendto(udp_result,address)
         print ("**********************************************")
         print ("200")
         print ("**********************************************")
         print ((rcode))
         print ((tcp_result))
         print ((udp_result))
         print ("**********************************************")
         print ("tcpresult!")
#     print (f"[RCODE]={rcode}")
#     print (f"**********************")
         #print ({tcp_result})
   
   else:
      print ("not a dns query")

###Execution
if __name__ == '__main__': ## Only executed when this is the main program
   DNS = '1.1.1.1'
   port = 35000
   host='192.168.1.229'
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #THIS IS UDP (SOCK_DGRAM)
      s.bind((host, port))
      while True:
        data,addr = s.recvfrom(1024)
        threading.Thread(target=requesthandle,args=(data, addr, DNS)).start
        #thread.start_new_thread(requesthandle,(data, addr, DNS))
        print ("88888888888888888888888888888888888888888888888888888888")
        print ((data))
        print ((addr))
        print ((DNS))
        print ("88888888888888888888888888888888888888888888888888888888")
        #print ("**[DATA]#"+{data}+"#[ADDR]: "+{addr}+"#[DNS]:"+{DNS}+"**")
   except Exception as e:
      print (e)
      s.close()


# TCP uses SOCK_STREAM and UDP uses SOCK_DGRAM.