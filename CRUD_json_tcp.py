from socket import *
import threading
import json

serverport = 12886
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverport))
serverSocket.listen(1)
print("Server is ready to recieve")
personList = []

# create: {"id":1,"name":"Eigil Moses IV Hammerby","address":"Sultestrejkevej 1","mobile":"22442244"}
# read
# update: 1 name Jyde
# delete: 1

def jsonCrudService(connectionSocket):
    while True:
        message = connectionSocket.recv(1024).decode().strip()
        if message == "exit":
            print("Exiting Service")
            break
        msg = message.split(": ")
        if msg[0] == "create" and len(msg) == 2:
            newObj = json.loads(msg[1])
            try:
                personList.append(newObj)
                outMessage = "New Person Created\n"
                connectionSocket.send(outMessage.encode())
            except json.JSONDecodeError:
                print("Argument needs to be in JSON format")
        elif msg[0] == "read":
            if len(personList) == 0:
                outMessage = "The list is empty\n"
                connectionSocket.send(outMessage.encode())
            for person in personList:
                outMessage = json.dumps(person)
                outMessage += "\n"
                connectionSocket.send(outMessage.encode())
        elif msg[0] == "update" and len(msg) == 2:
            args = msg[1].split()
            id = int(args[0])
            param = str(args[1])
            value = str(args[2])
            for person in personList:
                if id == int(person["id"]):
                    person[param] = value
                    break
            outMessage = "Person Updated\n"
            connectionSocket.send(outMessage.encode())
        elif msg[0] == "delete" and len(msg) == 2:
            id = int(msg[1])
            for person in personList:
                if id == person["id"]:
                    personList.remove(person)
                    break
            outMessage = "Person Removed\n"
            connectionSocket.send(outMessage.encode())
        

# {"create":{"id":1, "name":"Eigil Moses IV Hammerby", "address":"Sultestrejkevej 2", "mobile":"00112233"}}
# {"read":1}
# {"update":{"id":1, "param":"name", "val":"Broder Salsa"}}
# {"delete":{"id":0}}

def jsonInputCrudService(connectionSocket):
    while True:
        message = connectionSocket.recv(1024).decode().strip()
        if message == "exit":
            print("Exiting Service")
            break
        try:
            msg = json.loads(message)
            keyList = list(msg.keys())
            if keyList[0] == "create":
                paramJson = msg["create"]
                personList.append(paramJson)
                outMessage = "New Person Created\n"
                connectionSocket.send(outMessage.encode())
            elif keyList[0] == "read":
                if len(personList) == 0:
                    outMessage = "The list is empty\n"
                    connectionSocket.send(outMessage.encode())
                for person in personList:
                    outMessage = json.dumps(person)
                    outMessage += "\n"
                    connectionSocket.send(outMessage.encode())    
            elif keyList[0] == "update":
                entry = msg["update"]
                args = list(entry.keys())
                id = int(entry[args[0]])
                param = str(entry[args[1]])
                val = str(entry[args[2]])
                for person in personList:
                    if person["id"] == id:
                        person[param] = val
                outMessage = f"{param} is now updated to {val}\n"
                connectionSocket.send(outMessage.encode())
            if keyList[0] == "delete":
                entry = msg["delete"]
                args = list(entry.keys())
                id = int(entry[args[0]])
                found = None
                for person in personList:
                    if person["id"] == id:
                        found = person
                personList.remove(found)
                outMessage = "Person removed\n"
                connectionSocket.send(outMessage.encode())
        except json.decoder.JSONDecodeError:
            print("Incorrect format for the input - json format is required")
            break

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection established with {addr}")
    threading.Thread(target=jsonInputCrudService, args=(connectionSocket,)).start()
    #threading.Thread(target=jsonCrudService, args=(connectionSocket,)).start()
    break