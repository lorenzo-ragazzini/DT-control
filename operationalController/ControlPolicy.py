from typing import List, Dict, Any, Union, Iterable
from abc import ABC, abstractmethod
from warnings import warn

class ControlPolicy:
    # def __init__(self,controller=None):
    #     self.controller = controller        
    #     self.inputParameters:List[str] = list()
    #     self.controlParameters:Dict[str,Any] = dict()
    inputParameters:List[str] = list()
    controlParameters:Dict[str,Any] = dict()
    _controller = None
    def __call__(self,*args,**kwargs):
        return self.solve(*args,**kwargs)
    def getInputParamters(self):
        return self.inputParameters
    def getControlParamters(self):
        return self.controlParameters
    def setControlParamters(self,key:str,value:Any):
        if key in self.controlParameters.keys():
            self.controlParameters[key]=value
            setattr(self,key,value)
        else:
            msg=f'Cannot assign {value} to {key}. Control paramter {key} not found.'
            warn(message=msg,category=RuntimeWarning,stacklevel=int(10e10))
    @abstractmethod
    def solve(self,*args,**kwargs):
        pass