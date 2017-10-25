#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-
import socket
import os
import sys
def confere_retorno_do_servidor(num):
    if(num == 404 or num == 400 or num == 401 or num == 403):
        arq = open('erro.html', 'w')
        arq.write(num)
        arq.close()
        return False
    elif(num == 301):
        arq = open('errog.txt', 'w')
        arq.write(num)
        arq.close()
        return False
    else:
    	arq = open(formato_arquivo, 'w')
    	arq.write(num)
    	arq.close()
    	return True
if len(sys.argv) < 3:
	print "Uso: pyclient [servidor] [arquivo] [porta]", len(argv)
	raise SystemExit
cliente_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = sys.argv[1]
porta = int(sys.argv[2])
server = server.replace("http://", "")
server = server.split("/")
formato_arquivo = server[len(server) -1]
host = socket.gethostbyname(server[0])
orig = (host, porta)
cliente_socket_tcp.connect(orig) #con
msg = "GET "
for i in range(1, len(server)):
	msg = msg + '/' + server[i]
msg = msg + " " + 'HTTP/1.1\r\n'
cliente_socket_tcp.send(msg)
num = cliente_socket_tcp.recv(1048576)
print 'XD', num
confere_retorno_do_servidor(num)
cliente_socket_tcp.close()
