import SocketHandler as sh
import threading

if __name__ == '__main__':
    server = sh.SocketServer((sh.SocketHandler.HOST, sh.SocketHandler.PORT), sh.SocketHandler)
    with server:
        ip, port = server.server_address
        print('Server initialised at {}:{}'.format(ip, port))
        #server_thread = threading.Thread(target=server.serve_forever)
        #server_thread.daemon = True
        try:
            #server_thread.start()
            #print('Server loop running in thread:', server_thread.name)
            server.serve_forever()
        except Exception:
            server.shutdown()
