from typing import List, Dict, Any, Union, Iterable
from abc import ABC, abstractmethod

class ControlPolicy:
    # def __init__(self):
    #     self.inputParameters:List[str] = list()
    #     self.controlParameters:Dict[str,Any] = dict()
    inputParameters:List[str] = list()
    controlParameters:Dict[str,Any] = dict()
    def __call__(self,*args,**kwargs):
        pass
    def getInputParamters(self):
        return self.inputParameters
    def getControlParamters(self):
        return self.controlParameters
    def setControlParamters(self,key:str,value:Any):
        if key in self.controlParameters.keys():
            self.controlParameters[key]=value
            setattr(self,key,value)
        else:
            return 'error'