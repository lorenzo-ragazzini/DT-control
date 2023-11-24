import requests
import json
class DTInterface:
    def __init__(self,url):
        self.url = "http://" + url
    def new(self) -> str:
        return requests.get(self.url+'/new').content.decode()
    def clear(self,name:str=None):
        data = {'name': name}
        requests.post(self.url+'/clear',json=data)
    def interface(self,name,taskResourceInformation,controlUpdate,request):
        headers = {'Content-Type': 'application/json'}
        inputs = json.dumps({"name":name, "taskResourceInformation":taskResourceInformation, "controlUpdate":controlUpdate, "request":request})
        requests.post(self.url+'/run', json=inputs, headers=headers)
        return requests.get(self.url+'/run',name)