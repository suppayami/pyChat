import SocketServer
import json


HOST = "localhost"
PORT = 1902

class ListenServer(SocketServer.ThreadingTCPServer):
    pass
        
class ClientHandler(SocketServer.StreamRequestHandler):
    clients = []
    def handle(self):
        ClientHandler.clients.append(self)
        print("Connected: " + str(self.client_address))
        while True:
            data = self.read_data()
            if not data:
                print("Disconnected: " + str(self.client_address))
                break
            else:
                self.send_data(data)
    
    def read_data(self):
        return self.rfile.readline().strip()
        
    def send_data(self, data):
        data = str(self.client_address) + ": " + data + "\n"
        for client in ClientHandler.clients:
            client.wfile.write(data)
            client.wfile.flush()
        
server = ListenServer((HOST, PORT), ClientHandler)
server.serve_forever()
