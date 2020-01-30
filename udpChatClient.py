# Import socket module
from socket import *
import select
import sys
import threading
import queue
import random

def Receive(sock,recvPackets):
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
                    clientSocket.sendto(data.encode('utf-8'), c)

def SendData(socket):
    while True:
        data = input()
        if data == 'quit':
            break
        elif data=='':
            continue
        data = '['+name+']' + '->'+ data
        clientSocket.sendto(data.encode('utf-8'),(serverName, serverPort))
    clentSocket.sendto(data.encode('utf-8'),(serverName, serverPort))
    # clientSocket.close()

if __name__ == '__main__':
    serverName= 'localhost'
    serverPort = 12000
    port = 6097
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.bind(('localhost', port))

    clients = set()
    recvPackets = queue.Queue()

    name = input('Please enter username: ')
    if name == '':
        name = 'Guest'+str(random.randint(1000,9999))
        print('Your name is:'+name)
    clientSocket.sendto(name.encode('utf-8'),(serverName, serverPort))
    # threading.Thread(target=ReceiveData,args=(clientSocket,)).start()

    threads = []
    t1 = threading.Thread(target=Receive,args=(clientSocket,recvPackets))
    threads.append(t1)
    t2 = threading.Thread(target=SendData,args=(clientSocket, ))
    threads.append(t2)

    for t in threads:
        t.setDaemon(True)  # Daemon the thread
        t.start()
    for t in threads:
        t.join()
# os._exit(1)
