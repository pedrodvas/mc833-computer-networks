#import socket module
from socket import *
import sys # In order to terminate the program
import threading
def serve_content(connectionSocket, addr):
    print(f"new connection at {connectionSocket}: {addr}")
    try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = #Fill in start #Fill in end
            #Send one HTTP header line into socket
            #Fill in start
            #Fill in end
            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            #Send response message for file not found
            #Fill in start#Fill in end
            #Close client socket
            #Fill in start
            #Fill in end
            serverSocket.close()
            sys.exit()#Terminate the program after sending the corresponding data
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
    
