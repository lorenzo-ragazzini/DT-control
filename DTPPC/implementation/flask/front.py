import requests
import json
class DTInterface:
    def __init__(self,url,debug=False):
        self.url = "http://" + url
        self._debug = debug
    def new(self) -> str:
        return requests.get(self.url+'/new').content.decode()
    def clear(self,name:str=None):
        data = {'name': name}
        requests.post(self.url+'/clear',json=data)
    def interface(self,name,taskResourceInformation,controlUpdate,request):
        if self._debug:
            print("Sending request to DT: %s" % request)
        headers = {'Content-Type': 'application/json'}
        controlUpdate['ExecuteSchedule']['sequence'] = [controlUpdate['ExecuteSchedule']['sequence'][key] for key in taskResourceInformation['Order'].values()]
        inputs = json.dumps({"name":name, "taskResourceInformation":taskResourceInformation, "controlUpdate":controlUpdate, "request":request})
        res = requests.post(self.url+'/run', json=inputs, headers=headers)
        # res = requests.get(self.url+'/run',json=inputs,headers=headers) # inutile, ottieni lo stesso risultato
        return json.loads(res.content.decode())
        