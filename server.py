import SocketServer
import json
import threading


class ServerHandling(threading.Thread):
    server = None
    def run(self):
        ServerHandling.server = ListenServer(("", 1902), ClientHandler)
        ServerHandling.server.serve_forever()
        
class ClientHandling(threading.Thread):
    def __init__(self, handler):
        self.handler = handler
        threading.Thread.__init__(self)
        
    def run(self):
        while True:
            data = self.handler.read_data()
            if not data:
                print("Disconnected: " + str(self.handler.client_address))
                break
            self.handler.send_data(data)
            
class CommandHandling(threading.Thread):
    def run(self):
        while True:
            string = raw_input(" ")
            if string.upper() == "CLOSE":
                ServerHandling.server.shutdown()
                ServerHandling.server.server_close()
                break
            else:
                for client in ClientHandler.clients:
                    client.request.sendall("From server: " + string + "\n")

class ListenServer(SocketServer.ThreadingTCPServer):
    pass
        
class ClientHandler(SocketServer.StreamRequestHandler):
    clients = []
    def handle(self):
        ClientHandler.clients.append(self)
        print("Connected: " + str(self.client_address))

        clientHandling = ClientHandling(self)
        clientHandling.start()
        commandHandling.join()
    
    def read_data(self):
        return self.rfile.readline().strip().decode("utf-8")
        
    def send_data(self, data):
        data = data + "\n"
        data = str(self.client_address) + ": " + data
        for client in ClientHandler.clients:
            client.wfile.write(data)
            client.wfile.flush()
        
serverHandling = ServerHandling()
serverHandling.start()

commandHandling = CommandHandling()
commandHandling.start()
commandHandling.join()
