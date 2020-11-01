import win32com.client

class LeCroyHandler:
    scope = None
    def __init__(self, address):
        if self.scope is not None:
            return
        self.scope = win32com.client.Dispatch('LeCroy.ActiveDSOCtrl.1')
        self.scope.MakeConnection('IP:{}'.format(address))
        ret = self.inquire('*IDN?')
        print('Connected to scope:', ret)
        self.send('*CLS') # clear status registers
        #self.send('C1:VDIV .200')
    def disconnect(self):
        self.scope.Disconnect()
        self.scope = None
    def beep(self):
        self.send('BUZZ BEEP')
    def send(self, cmd):
        self.scope.WriteString(cmd, True)
    def inquire(self, cmd):
        if type(cmd) == list:
            cmd = ' '.join(cmd)
        self.send(cmd)
        return self.scope.ReadString(80)
    def acquire_data(self, ch_id, num_seq=10):
        if ch_id < 1 or ch_id > 4:
            raise Exception('ERROR:BAD_CHANNEL')
        self.send('STORE C{},FILE'.format(ch_id))
        self.send('SEQUENCE ON,10,{}'.format(num_seq))
        self.send('ARM_ACQUISITION')
    def get_data(self, ch_id):
        return self.scope.GetScaledWaveform('C{}'.format(ch_id), 5000, 0)

if __name__ == '__main__':
    handler = LeCroyHandler('localhost')
    print(handler.inquire('*IDN?'))
