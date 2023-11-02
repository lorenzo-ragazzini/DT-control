# -*- coding: utf-8 -*-
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

class ControlMap:
    def __init__(self):
        self.rules:Dict[str,ControlRule] = dict()
    def __call__(self,event):
        for key in self.rules.keys():
            self.rules[key](event)

class ControlRule:
    def __init__(self):
        self.target:Dict[str,Iterable[ControlPolicy]] = dict()
    def __call__(self,event) -> Iterable[ControlPolicy]:
        self.run(event)
    @abstractmethod
    def run(self) -> Iterable[ControlPolicy]:
        pass

class OperationalController:
    def __init__(self):
        self.map:ControlMap = None
        self.policies:List[ControlPolicy] = [None]
    def send(self,event):
        policies:Iterable[ControlPolicy] = self.map(event)
        for cp in policies:
            self._execute(cp)
    def _execute(self,cp:ControlPolicy):
            pars = cp.getInputParamters()
            input = self._search(Iterable[str])
            dv = cp(input)
    @abstractmethod
    def _search(self,input:str) -> List[Any]:
        pass