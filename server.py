import threading
import socket

host = "127.0.0.1" #localhost
port = 55555 #anything above 1024

server= socket.socket(socket.AF_INET,socket.SOCK_STREAM) #internet ipv4 and tcp
server.bind((host, port)) #bind server to host and ip address
server.listen() #server listens for new incoming connections

clients =[]
nicknames =[] #client's nickname

#broadcast, sends msg to all clients that are currently connected to server
def broadcast(message):
    for client in clients:
        client.send(message)

#handle clients's connections. send msgs and send back msg to other clients in broadcast
def handle(client):
    while True:
        try:
            message = client.recv(1024) #try to receive a msg from a client, then broadcast it to every client
            broadcast(message)
        except: #if there is error while receiving msg or broadcasting
            index= clients.index(client) #need client's index in order to remove them
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('asci')) #tell everyone that this client has left
            nicknames.remove(nickname)
            break

#combines all the functions

def receive():
    while True: #accept clients all the time
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address))) #if client connects, print on server console

        # Request And Store Nickname
        client.send('NICK'.encode('ascii')) #ask client for nickname
        nickname = client.recv(1024).decode('ascii') #the msg recieved is the nickname
        nicknames.append(nickname) #we save the values in the list
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii')) #tell all the clients that this new client joined
        client.send('Connected to the server!'.encode('ascii'))  #tell the client that they are connected so they can start chatting

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,)) #run one thread for each client
        thread.start()
print("Server is listening...")
receive()