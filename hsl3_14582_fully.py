import json
import requests

class LogicModule:

    def __init__(self, hsl3):
        self.fw = hsl3
        self.debug = self.fw.create_debug_section()

    def on_init(self, inputs, store):
        pass

    def on_calc(self, inputs):
        self.hostname = inputs["server_name"].value.decode('utf-8')
        self.password = inputs["password"].value.decode('utf-8')
        self.port = int(inputs["port"].value)
        self.protocol = 'https' if inputs["ssl"].value else 'http'
        
        if inputs["restart_app"].changed and inputs["restart_app"].value != 0:
            self.restartApp()
        if inputs["on"].changed:
            self.screenOn(inputs["on"].value != 0)
        if inputs["brightness"].changed:
            self.brightness(inputs["brightness"].value)

    def restartApp(self):
        self.sendCmd('restartApp')
        
    def screenOn(self, on):
        if (on):
            self.sendCmd('screenOn')
        else:
            self.sendCmd('screenOff')

    def brightness(self, percentage):
        value = int(round(percentage*2.55))
        self.sendCmd('setStringSetting&key=screenBrightness&value=%d' % value)

    def sendCmd(self, cmd):
        url='{}://{}:{}/?cmd={}&password={}&type=json'.format(
            self.protocol, self.hostname, self.port, cmd, self.password)

        try:
            response = requests.get(url, verify=False)
            j=json.loads(response.text)

            self.fw.set_output("ok", int(j['status'] == 'OK'))
            self.fw.set_output("msg", j['statustext'].encode('utf-8'))
            #self.debug.log("Response: {}".format(j))

        except Exception as e:
            self.debug.log("Error: {}".format(e))
            self.fw.set_output("ok", 0)
            self.fw.set_output("msg", "Error: {}".format(e).encode('utf-8'))
