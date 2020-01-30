# Import socket module
from socket import *
import select
import sys
import threading
import queue

def SendData(socket):
    while True:
        data = input()
        if data == 'quit':
            break
        elif data=='':
            continue
        data = '['+name+']' + '->'+ data
        serverSocket.sendto(data.encode('utf-8'),('localhost', 6097))

def Receive(sock, recvPackets):
    while True:
        data,addr = sock.recvfrom(2048)
        recvPackets.put((data,addr))
        while not recvPackets.empty():
            data,addr = recvPackets.get()
            if addr not in clients:
                clients.add(addr)
                continue
            clients.add(addr)
            data = data.decode('utf-8')
            if data.endswith('quit'):
                clients.remove(addr)
                continue
            print(str(addr)+data)
            for c in clients:
                if c!=addr:
                    serverSocket.sendto(data.encode('utf-8'), c)

if __name__ == '__main__':
    # Assign a port number
    serverPort = 12000
    # Create a UDP server socket
    # (AF_INET is used for IPv4 protocols)
    # (SOCK_DGRAM) is used for UDP
    serverSocket = socket(AF_INET,SOCK_DGRAM)
    # Bind the socket to server address and server port
    serverSocket.bind(('localhost',serverPort))

    clients = set()
    recvPackets = queue.Queue()

    print('The server is ready to receive')
    name = input('Please enter username: ')
    if name == '':
        name = 'Guest'+str(random.randint(1000,9999))
        print('Your name is:'+name)
    serverSocket.sendto(name.encode('utf-8'),('localhost', 6097))

    threads = []
    t1 = threading.Thread(target=Receive,args=(serverSocket,recvPackets))
    threads.append(t1)
    t2 = threading.Thread(target=SendData,args=(serverSocket, ))
    threads.append(t2)

    for t in threads:
        t.setDaemon(True)  # Daemon the thread
        t.start()

    for t in threads:
        t.join()
# serverSocket.close()
