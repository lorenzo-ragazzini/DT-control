from typing import List, Dict, Any, Union, Iterable, Type
from abc import ABC, abstractmethod
import json
from collections import ChainMap
from .controlMap import ControlMap
from .controlPolicy import ControlPolicy
from .controlModule import ControlModule

class OperationalController:
    map:ControlMap
    policies:Iterable[ControlPolicy] = list()
    modules:Iterable[ControlModule] = list()
    decisionVariables = DecisionVariables()
    systemModel = {}
    def addPolicy(self,Cp:Type[ControlPolicy]):
        self.policies.append(Cp(self))
    def addModule(self,Cm:Type[ControlModule]):
        self.modules.append(Cm(self))
    def linkPolicies(self):
        for cp in self.policies+self.modules:
            cp._controller = self
    def send(self,event):
        policies:Iterable[Type[Union[ControlPolicy,ControlModule]]] = self.map(event)
        for cp in policies:
            self.execute(self[cp])
    def execute(self,c:ControlPolicy):
        pars = c.getInputParamters()
        input = self.search(pars)
        if issubclass(type(c),ControlPolicy):
            dv = c(input=input)
            self.decisionVariables.update(dv)
            self.saveDecisionVariables()
        else:
            policies = c(input=input)
            for cc in policies:
                self.execute(self[cc])
    def saveDecisionVariables(self):
        with open('dv.json', 'w') as f: 
            json.dump(self.decisionVariables, f)
    def search(self,input:Iterable[str]) -> List[Any]:
        return dict(ChainMap(*[{el:self.systemModel[el]} for el in input]))
    def __getattr__(self,attr):
        try:
            value = [p for p in self.policies+self.modules if p.__class__.__name__ is attr]
            if not value:
                raise AttributeError
            else:
                return value[0]
            return [p for p in self.policies+self.modules if p.__class__.__name__ is attr]
        except:
            object.__getattribute__(self,attr)
    def __getitem__(self,item):
        if type(item) is type:
            return self.__getattr__(item.__name__)

class DecisionVariables(dict):
    def __init__(self, *args, **kwargs):
        self._callback = None
        super().__init__(*args, **kwargs)
    def set_callback(self, callback):
        self._callback = callback
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        if self.get(key) != value:
            super().__setitem__(key, value)
            if self._callback:
                self._callback(key, value)