import socket
import thread
import os


HOST = "localhost"
PORT = 1902

def read_data(sock):
    rb = sock.makefile("rb", -1)
    return rb.readline().strip().decode("utf-8")
    
def send_data(sock, data):
    sock.sendall(data)
    
def fetchData():
    while True:
        data = read_data(sock)
        if data:
            backlog.append(data)
            os.system(['clear','cls'][os.name == 'nt'])
            for line in backlog:
                print(line)
        
sock = socket.socket()
backlog = []
try:
    sock.connect((HOST, PORT))
    thread.start_new_thread(fetchData, ())   
    while True:
        string = raw_input("")
        string = string + "\n"
        send_data(sock, string)

except:
    sock.close()
