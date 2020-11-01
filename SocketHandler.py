import socketserver
import socket
import LeCroyHandler

class SocketHandler(socketserver.BaseRequestHandler):
    HOST = socket.gethostname()
    PORT = 4040
    ENCODING = 'utf-8'
    def setup(self):
        self.scope = None
    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            if not self.data:
                break
            sequence = self.data.decode(self.ENCODING).split(' ')
            arguments = ' '.join(sequence[1:])
            command = sequence[0].lower()
            print('{} wrote: {}'.format(self.client_address[0], self.data))
            if 'quit' in command:
                self.quit_smoothly()
            elif 'scope' in command:
                self.parse_scope_command(arguments)
    def finish(self):
        self.quit_smoothly()
    def to_command(self, cmd):
        if type(cmd) == list:
            cmd = ' '.join(cmd)
        return bytes(cmd, self.ENCODING)
    def parse_scope_command(self, args):
        if self.scope is None:
            self.scope = LeCroyHandler.LeCroyHandler(self.HOST)
            self.send('CONNECTED')
        sequence = args.split(' ')
        arguments = ' '.join(sequence[1:])
        command = sequence[0].lower()
        if 'beep' in command:
            self.scope.beep()
        elif 'acq' in command:
            ch_id = -1
            num_seq = 10
            if len(sequence) > 1:
                ch_id = int(sequence[1])
            if len(sequence) > 2:
                num_seq = int(sequence[2])
            try:
                self.scope.acquire_data(ch_id, num_seq)
            except Exception as err:
                self.send(err.message())
            self.send('ACQUIRED')
        elif 'wave' in command:
            ch_id = -1
            if len(sequence) > 1:
                ch_id = int(sequence[1])
            waveform = self.scope.get_data(ch_id)
            self.send(str(waveform))
        elif 'send' in command:
            self.scope.send(sequence[1:])
        elif 'recv' in command:
            ret = self.scope.inquire(arguments)
            self.send(ret)
        elif 'end' in command:
            self.disconnect_scope()
    def disconnect_scope(self):
        if self.scope is not None:
            self.scope.disconnect()
            self.send('DISCONNECTED')
        self.scope = None
    def send(self, cmd):
        self.request.sendto(self.to_command(cmd+'\n'), self.client_address)
    def quit_smoothly(self):
        self.disconnect_scope()
        self.request.sendall(b'SHUTDOWN\n')
        raise Exception('Shutdown requested')

class SocketServer(socketserver.TCPServer):
    pass
    
