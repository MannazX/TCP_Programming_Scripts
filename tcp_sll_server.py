from socket import *
import threading
import ssl

serverport = 12538
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverport))
serverSocket.listen(1)
print("Server is ready to recieve")

certificatesDirectory = "C:\certificates"
privateKeyPath = certificatesDirectory + "\key.pem"
certificatePath = certificatesDirectory + "\certificate.pem"
print("Please enter password: ")
privateKeyPassword = input()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=certificatePath, keyfile=privateKeyPath, password=privateKeyPassword)
secureSocket = context.wrap_socket(serverSocket)

def regneService(connectionSocket):
    while True:
        message = connectionSocket.recv(1024).decode().strip()
        if message == "exit":
            print("Exiting Service")
            break
        msg = message.split()
        response = ""
        if msg[0] == "add" and len(msg) > 2:
            sum = int(msg[1]) + int(msg[2])
            response = str(sum)
        if msg[0] == "subtract" and len(msg) > 2:
            sum = int(msg[1]) - int(msg[2])
            response = str(sum)
            
        print(f"Recieved Message: {message}")
        response = response + "\n"
        connectionSocket.send(response.encode())
        print(f"Message sent back {response}\n")
        
while True:
    connectionSocket, addr = secureSocket.accept()
    print(f"Connection established with {addr}")
    #threading.Thread(target=service, args=(connectionSocket,)).start()
    threading.Thread(target=regneService, args=(connectionSocket,)).start()
    #threading.Thread(target=jsonRegneService, args=(connectionSocket,)).start()
    
    break

