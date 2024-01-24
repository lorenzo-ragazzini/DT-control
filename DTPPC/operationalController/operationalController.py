from typing import List, Dict, Any, Union, Iterable, Type
from abc import ABC, abstractmethod
import json
from collections import ChainMap
from .controlMap import ControlMap
from .controlPolicy import ControlPolicy
from .controlModule import ControlModule
from .decisionVariables import DecisionVariables

class OperationalController:
    map:ControlMap
    policies:Iterable[ControlPolicy] = list()
    modules:Iterable[ControlModule] = list()
    decisionVariables:DecisionVariables = DecisionVariables()
    systemModel = {}
    _debug = False
    def addPolicy(self,Cp:Type[ControlPolicy]):
        self.policies.append(Cp(self))
    def addModule(self,Cm:Type[ControlModule]):
        self.modules.append(Cm(self))
    def linkPolicies(self):
        for cp in self.policies+self.modules:
            cp._controller = self
    def linkRules(self):
        self.map._controller = self
        for rule in self.map.rules:
            rule._controller = self
            rule._map = self.map
    def send(self,event):
        if self._debug == True:
            print("Controller received event: %s" % event)
        policies:Iterable[Type[Union[ControlPolicy,ControlModule]]] = self.map(event)
        for cp in policies:
            self.execute(self[cp])
    def execute(self,c:ControlPolicy) -> Union[None,DecisionVariables]:
        if self._debug == True:
            print('Executing %s' % c)
        pars = c.getInputParamters()
        input = self.search(pars)
        if issubclass(type(c),ControlPolicy):
            dv = c(input=input)
            if dv is not None:
                if self._debug == True:
                    print("Updating decision variable: %s" % dv)
                self.decisionVariables.update(dv)
                self.saveDecisionVariables()
            return dv
        else:
            policies = c(input=input)
            for cc in policies:
                self.execute(self[cc])
            return
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