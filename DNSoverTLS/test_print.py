import socket
import ssl
import sys

import threading      
#from thread import *
import binascii
import codecs

tcp_result ='00405ec8818000010002000000000377777706707265706c7903636f6d0000010001c00c000100010000012c0004681214b4c00c000100010000012c0004681215b4'


#dn=int(dns_query,16)
print (type(tcp_result))
rcode = str(tcp_result[:6])
print (rcode) # 303034303565

rcode = str(rcode)[11:]
print str(rcode)

"""print ("------")
print(rcode).encode("hex")
print ("------")
rcode2 = str(rcode)[11:]
print ("++++++")
print(rcode2).encode("hex")
print ("+++++")"""

""" print (ldnsq)
print (chrldnsq)
print ("------")
print (pre_length)
#binascii.hexlify (pre_length)
print (bytes_length.hex())
#codecs.encode(pre_length,'hex_codec')
print ("*******") """

