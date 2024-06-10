import json

class FileJson:
    def __init__(self,fname = 'data\\data.json'):
        self.file_name = fname
        self.rdata = None
        self.activeprog = self.finde_active_prog()

    def rjson(self):
        with open(self.file_name,'r') as f:
            data = json.load(f)
            return data

    def wjson(self,data):
        with open(self.file_name,'w') as f:
            json.dump(data, f, indent = 4)

    def finde_active_prog(self):
        self.rdata = self.rjson()
        activeprog = [key for key, obj in self.rdata.items() if obj["state"] == 1]
        self.activeprog = activeprog[0]
        return self.activeprog
    
    def sprogname(self, newprog):
        if newprog != self.finde_active_prog():
            self.rdata[self.activeprog]["state"] = 0
            self.rdata[newprog]["state"] = 1
            self.wjson(self.rdata)

