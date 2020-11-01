import socketserver
import socket
import LeCroyHandler
import win32com.client

HOST = socket.gethostname()
PORT = 4040
ENCODING = 'utf-8'

class SocketHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.scope = None
    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            if not self.data:
                break
            sequence = self.data.decode(ENCODING).split(' ')
            arguments = ' '.join(sequence[1:])
            command = sequence[0].lower()
            print('{} wrote: {}'.format(self.client_address[0], self.data))
            if 'quit' in command:
                self.quit_smoothly()
            elif 'scope' in command:
                if self.scope is None:
                    self.scope = LeCroyHandler.LeCroyHandler(HOST)
                    self.send('CONNECTED')
                if len(sequence) > 1:
                    if 'beep' in arguments:
                        self.scope.beep()
                    elif 'acq' in arguments:
                        ch_id = -1
                        num_seq = 10
                        if len(sequence) > 2:
                            ch_id = int(sequence[2])
                        if len(sequence) > 3:
                            num_seq = int(sequence[3])
                        try:
                            self.scope.acquire_data(ch_id, num_seq)
                        except Exception as err:
                            self.send(err.message())
                    elif 'wave' in arguments:
                        ch_id = -1
                        if len(sequence) > 2:
                            ch_id = int(sequence[2])
                        waveform = self.scope.get_data(ch_id)
                        self.send(str(waveform))
                    elif 'send' in arguments:
                        self.scope.send(sequence[2:])
                    elif 'recv' in arguments:
                        ret = self.scope.inquire(sequence[2:])
                        self.send(ret)
                    elif 'end' in arguments:
                        self.scope.disconnect()
                        self.scope = None
                        self.send('DISCONNECTED')
    def to_command(self, cmd):
        if type(cmd) == list:
            cmd = ' '.join(cmd)
        return bytes(cmd, ENCODING)
    def send(self, cmd):
        self.request.sendto(self.to_command(cmd+'\n'), self.client_address)
        
    def quit_smoothly(self):
        self.request.sendall(b'SHUTDOWN\n')
        raise Exception('Shutdown requested')

if __name__ == '__main__':
    server = socketserver.TCPServer((HOST, PORT), SocketHandler)
    try:
        server.serve_forever()
    except Exception:
        server.shutdown()
