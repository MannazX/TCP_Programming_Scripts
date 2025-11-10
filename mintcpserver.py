from socket import *
import threading
import json

serverport = 12540
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverport))
serverSocket.listen(1)
print("Server is ready to recieve")

def jsonRegneService(connectionSocket):
    while True:
        message = connectionSocket.recv(1024).decode().strip()
        if message == "exit":
            print("Exiting Service")
            break
        try:
            msg = json.loads(message)
            result = {}
            if len(msg.items()) > 2:
                if msg["operation"] == "add":
                    result["result"] = int(msg["number1"]) + int(msg["number2"])
                if msg["operation"] == "subtract":
                    result["result"] = int(msg["number1"]) - int(msg["number2"])
            else:
                print("Need more than two arguments")
            print(f"Recieved Message: {message}")
            response = json.dumps(result)
            response = response + "\n"
            connectionSocket.send(response.encode())
            print(f"Message sent back {response}\n")
        except json.decoder.JSONDecodeError:
            print("Incorrect format for this service - json format required")
            break
        

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
        

def service(connectionSocket):
    while True:
        message = connectionSocket.recv(1024).decode().strip()
        if message == "exit":
            print("Exiting Service")
            break
        msg = message.split()
        response = ""
        if msg[0] == "upper":
            response = " ".join(msg[1:]).upper()
        if msg[0] == "echo":
            response = " ".join(msg[1:])
        if msg[0] == "double":
            response = " ".join(msg[1:])*2
        
        print(f"Recieved Message: {message}")
        response = response+"\n"
        connectionSocket.send(response.encode())
        print(f"Message sent back {response}\n")
        
while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection established with {addr}")
    #threading.Thread(target=service, args=(connectionSocket,)).start()
    threading.Thread(target=regneService, args=(connectionSocket,)).start()
    #threading.Thread(target=jsonRegneService, args=(connectionSocket,)).start()
    
    break
