#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-
import socket
import os
import sys
import re

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
msg = msg + " " + 'HTTP/1.1\nHost:' + host + '\nConnection: close\nUser-agent:Mozilla/5.0\n\n'
cliente_socket_tcp.send(msg)
num = cliente_socket_tcp.recv(1048576)
pe = ["404 Not Found", "502 Bad Gateway", "400 Bad Request", "301 Moved Permanently" ]
error = False
for i in range (0, 3):
    if(re.search(pe[i], num)):
        error = True
        arq1 = open('erro.html', 'w')
        arq1.write(pe[i])
        arq1.close()
        break
if(error is False):
    num.split("\n\r\n")
    cabecalho = num[0]
    resto = ""
    for i in range(1, len(num)):
        resto = resto + num[i]

arq = open(server[(len(server))-1], 'w')
arq.write(resto)
arq.close()
cliente_socket_tcp.close()
