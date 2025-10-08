from socket import *
import threading
import json

class Person:
    def __init__(self, id: int, name: str, address: str, phoneNo: str):
        self.id = id
        self.name = name
        self.address = address
        self.phoneNo = phoneNo
        
    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Address: {self.address}, Phone No.: {self.phoneNo}"

serverport = 12558
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverport))
serverSocket.listen(2)
print("Server is ready to recieve")

p1 = Person(1, "Eigil Moses IV Hammerby", "Sultestrejkevej 2", "00112233")
person_list = [p1]
person_list.append(p1)
def crudService(connectionSocket):
    while True:
        message = connectionSocket.recv(1024).decode().strip()
        if message == "exit":
            print("Exiting Service")
            break
        msg = message.split()
        response = ""
        if msg[0] == "create" and len(msg) == 5:
            person_id = int(msg[1]); person_name = msg[2]; person_address = msg[3]; person_phone = msg[4]
            new_person = Person(person_id, person_name, person_address, person_phone)
            person_list.append(new_person)
            response = "New person added to the list"
        elif msg[0] == "read" and len(msg) == 2:
            list_idx = int(msg[1])
            for item in person_list:
                if item.id == list_idx:
                    response = str(item)
                    print(response)
        elif msg[0] == "update name" and len(msg) == 3:
            list_idx = int(msg[1])
            new_name = msg[2]
            person_list[list_idx].name = new_name
            response = f"Name has been changed to {new_name}"
        elif msg[0] == "update address" and len(msg) == 3:
            list_idx = int(msg[1])
            new_address = msg[2]
            person_list[list_idx].address = new_address
            response = f"Name has been changed to {new_address}"
        elif msg[0] == "delete" and len(msg) == 2:
            list_idx = int(msg[1])
            person_list.remove(person_list[list_idx])
            response = f"Item at index {list_idx} has been removed"
        print(f"Recieved Message {message}")
        response = response + "\n"
        connectionSocket.send(response.encode())
        print(f"Message sent back\n{response}")
            
while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection established with {addr}")
    threading.Thread(target=crudService, args=(connectionSocket,)).start()
    break