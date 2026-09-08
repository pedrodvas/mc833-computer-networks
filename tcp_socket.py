#import socket module
from socket import *
import sys # In order to terminate the program
import threading
import mimetypes
import os

def serve_content(connectionSocket, addr):
    print(f"new connection at {connectionSocket}: {addr}")
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        filepath = filename[1:] if filename != '/' else 'index.html'
        full_filepath = os.path.join(r"C:\Users\pdvsp\Downloads", filepath)
        with open(full_filepath, 'rb') as f:
            outputdata = f.read()

        content_type, _ = mimetypes.guess_type(full_filepath)
        if content_type is None:
            content_type = "application/octet-stream"
        header = f"HTTP/1.1 200 OK\r\n"
        header += f"Content-Type: {content_type}\r\n"
        header += f"Content-Length: {len(outputdata)}\r\n"
        header += "Connection: close\r\n\r\n"
        
        connectionSocket.sendall(header.encode())
        connectionSocket.sendall(outputdata)
        connectionSocket.close()
    except IOError:
        body = "<html><body><h1>404 Not Found</h1></body></html>\r\n"
        header_404 = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            "Connection: close\r\n\r\n"
        )
        connectionSocket.sendall(header_404.encode())
        connectionSocket.sendall(body.encode())
        connectionSocket.close()
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverPort = 6767 #which port 
serverSocket.bind(('', serverPort)) #allowing traffic from anywhere inside my network
serverSocket.listen(3)
#Fill in start
#Fill in end
while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    thread = threading.Thread(target=serve_content, args=(connectionSocket, addr))
    thread.start()
    #here, we have a new connection made, and we have to create
    #a new thread to deal with it
    
