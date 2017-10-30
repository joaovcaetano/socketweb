#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-
import socket
import thread
import os
import sys

HOST = ''              # Endereco IP do Servidor
pasta = sys.argv[1]
porta = int(sys.argv[2])
def contentType(arq):
    ext = arq.split(".")
    if ext[-1] == "html":
        return "text/HTML"
    elif ext[-1] == "txt":
        return "text/txt"
    elif ext[-1] == "jpg":
        return "image/jpg"
    elif ext[-1] == "png":
        return "image/png"
    elif ext[-1] == "gif":
        return "image/gif"
    elif ext[-1] == "ico":
        return "image/ico"
    elif ext[-1] == "css":
        return "text/css"
def conectado(con, cliente):
    print 'Cliente Conectado', cliente

    while True:
        msg = con.recv(1024) #servidor aguardando conexões
        if not msg: break
        print msg
        msg = msg.split(" ")
        print msg[1]
        arquivo = msg[1]
        print arquivo
        arquivo = arquivo.replace("/", "")
        print "ola", arquivo
        print "oi", os.listdir(pasta)
        if(arquivo in os.listdir(pasta)):
        	lenght = os.path.getsize(pasta)
        	print "XDXD"
        	saida = "HTTP/1.1 "+"200"+" OK\r\nContent-Type: "+ contentType(arquivo)+"\r\nContent-Length: "+str(lenght)+"\r\n\r\n"
        	arq = open(pasta + "/" +arquivo,'r')
        	dado = arq.read()
        	print "oioio", saida+dado
        	con.send(saida+dado)
        	con.close()
        else:
        	lenght = os.path.getsize(pasta)
        	mensagem = "ERROR"
        	con.send("ERROR")

        

    print 'Conexao Encerrada', cliente
    con.close()
    thread.exit()

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
origem = (HOST, porta)
serv_socket.bind(origem)
serv_socket.listen(1) #servidor escutando na porta 7777

while True:
    con, cliente = serv_socket.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
