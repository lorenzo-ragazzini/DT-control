import requests

class DTInterface:
    def __init__(self,url):
        self.url = url
    def new(self):
        return requests.get(self.url+'/new')
    def clear(self,name:str=''):
        requests.post(self.url+'/clear',name)
    def run(self,name,inputs):
        requests.post(self.url+'/run',inputs)
        return requests.get(self.url+'/results',name)