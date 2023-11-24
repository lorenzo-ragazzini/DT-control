import requests

class DTInterface:
    def __init__(self,url):
        self.url = "http://" + url
    def new(self):
        return requests.get(self.url+'/new')
    def clear(self,name:str=None):
        data = {'name': name}
        requests.post(self.url+'/clear',json=data)
    def run(self,name,inputs):
        requests.post(self.url+'/run',inputs)
        return requests.get(self.url+'/results',name)