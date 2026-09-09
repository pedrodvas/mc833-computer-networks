from socket import *
import threading
import mimetypes
import os
import time

# Constantes de configuracao para controle de taxa (Rate Limiting)
CHUNK_SIZE = 1024  # Envio de 1 KB por bloco
DELAY = 0.5        # Pausa de 500 ms entre envios para evidenciar a concorrencia

def serve_content(connectionSocket, addr):
    """
    Funcao executada em thread dedicada para cada cliente conectado.
    Processa a requisicao HTTP GET, le o recurso do disco e transmite a resposta.
    """
    print(f"Nova conexao estabelecida: {addr}")
    filepath = "unknown"
    try:
        # Recebe os bytes da requisicao HTTP enviada pelo navegador
        message = connectionSocket.recv(1024).decode()
        parts = message.split()
        
        # Faz o parsing do metodo HTTP GET e extrai o recurso solicitado
        if len(parts) >= 2:
            filename = parts[1]
            # Mapeia requisicao raiz '/' para index.html
            filepath = filename[1:] if filename != '/' else 'index.html'
        else:
            filepath = 'index.html'
            
        # Leitura do arquivo em modo binario para preservar integridade de midias/PDFs
        with open(filepath, 'rb') as f:
            outputdata = f.read()

        # Identifica dinamicamente o Content-Type a partir da extensao
        content_type, _ = mimetypes.guess_type(filepath)
        if content_type is None:
            content_type = "application/octet-stream"
            
        # Montagem dos cabecalhos padrao HTTP/1.1 de sucesso (200 OK)
        header = f"HTTP/1.1 200 OK\r\n"
        header += f"Content-Type: {content_type}\r\n"
        header += f"Content-Length: {len(outputdata)}\r\n"
        header += "Connection: close\r\n\r\n"
        
        # Envia a linha de status e cabecalhos
        connectionSocket.sendall(header.encode())

        # Envia o corpo fatiado em pedacos com delay para demonstracao visual de concorrencia
        for i in range(0, len(outputdata), CHUNK_SIZE):
            chunk = outputdata[i:i+CHUNK_SIZE]
            connectionSocket.sendall(chunk)
            time.sleep(DELAY)
            
        # Encerra o socket do cliente apos o termino da transmissao
        connectionSocket.close()
        print(f"Envio finalizado com sucesso para: {addr}")
        
    except IOError:
        # Tratamento de erro quando o arquivo nao existe no diretorio local (404 Not Found)
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

# Inicializacao do socket TCP
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6767

# Associa o socket a porta 6767 em todas as interfaces de rede disponiveis
serverSocket.bind(('', serverPort))
serverSocket.listen(3)

print("Servidor HTTP ativo e pronto para receber conexoes...")

# Laco principal: aceita conexoes e despacha imediatamente para threads filhas
while True:
    connectionSocket, addr = serverSocket.accept()
    # Cria uma nova thread para atender o cliente, liberando o laco principal
    thread = threading.Thread(target=serve_content, args=(connectionSocket, addr))
    thread.start()