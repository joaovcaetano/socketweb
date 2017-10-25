#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-
import socket
import thread
import os
import sys

HOST = ''              # Endereco IP do Servidor

def conectado(con, cliente):
    print 'Cliente Conectado', cliente

    while True:
        msg = con.recv(1024) #servidor aguardando conexões
        if not msg: break
        print msg
        dirs = os.listdir(msg)
        for i in range(0, len(dirs)):
            print dirs[i]
        print cliente, msg

    print 'Conexao Encerrada', cliente
    con.close()
    thread.exit()

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
origem = (HOST, 8080)
serv_socket.bind(origem)
serv_socket.listen(1) #servidor escutando na porta 7777

while True:
    con, cliente = serv_socket.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
