from socket import *
import threading
import mimetypes
import os
import time

CHUNK_SIZE = 1024 #1 kilobyte per chunk
DELAY = 0.5 #half a second
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def serve_content(connectionSocket, addr):
    print(f"new connection at {connectionSocket}: {addr}")
    filepath = "unknown"
    try:
        message = connectionSocket.recv(1024).decode()
        parts = message.split()
        if len(parts) >= 2:
            filename = parts[1]
            filepath = filename[1:] if filename != '/' else 'index.html'
        else:
            filepath = 'index.html'
        full_filepath = os.path.abspath(os.path.join(BASE_DIR, filepath))
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

        #connectionSocket.sendall(outputdata)
        #solution below used just to show concurrency
        for i in range(0, len(outputdata), CHUNK_SIZE):
            chunk = outputdata[i:i+CHUNK_SIZE]
            connectionSocket.sendall(chunk)
            time.sleep(DELAY)
        connectionSocket.close()
        print(f"envio terminado")
    except IOError:
        body = (f"<html><body><h1>404 Not Found</h1>"
                f"<p>O recurso solicitado <code>/{filepath}</code> nao foi encontrado neste servidor.</p></body></html>\r\n")
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
    
