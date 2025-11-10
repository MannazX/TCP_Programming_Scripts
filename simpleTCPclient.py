# computer networks TCPClient, page 191
from socket import *
import ssl

serverport = 12538
servername = "localhost"

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((servername, serverport))
while True:
  
  request = input('Enter request: ')
  clientSocket.send(request.encode())
  response = clientSocket.recv(1024).decode()
  print(f'Response from server: {response}')
  if request.lower() == 'exit':
      print('Exiting client.')
      break
    
clientSocket.close()