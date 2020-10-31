import socketserver
import socket
import win32com.client

HOST = socket.gethostname()
PORT = 4040

class LeCroyHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            self.data = self.rfile.readline()
            if not self.data:
                break
            self.data = self.data.strip().lower()
            print(self.data)
            if self.data == b'quit':
                self.quit_smoothly()
            if self.data == b'scope':
                self.connect_scope()
    def connect_scope(self):
        SCOPE_ADDRESS = HOST
        SCOPE_PORT = 1861
        self.scope = win32com.client.Dispatch('LeCroy.ActiveDSOCtrl.1')
        self.scope.MakeConnection('IP:{}'.format(HOST))
    def disconnect_scope(self):
        self.scope.Disconnect()
    def quit_smoothly(self):
        self.shutdown()

if __name__ == '__main__':
    server = socketserver.TCPServer((HOST, PORT), LeCroyHandler)
    server.serve_forever()
