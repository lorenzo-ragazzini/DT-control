from typing import List, Dict, Any, Union, Iterable, Type
from abc import ABC, abstractmethod
from .controlPolicy import ControlPolicy
from .controlModule import ControlModule

class ControlRule:
    trigger:None
    target:Iterable[Type]
    def __init__(self) -> None:
        self._controller = None
        self._controlMap = None
    def __call__(self,event) -> Iterable[Union[ControlPolicy,ControlModule]]:
        if event == self.trigger:
            return self.run(event)
        else:
            return []
    @abstractmethod
    def run(self,event) -> Iterable[Union[ControlPolicy,ControlModule]]:
        return None
    
'''
class ControlRule:
    trigger:None
    target:Dict[str,Iterable[Union[ControlPolicy,ControlModule]]]
    def __call__(self,event) -> Iterable[ControlPolicy]:
        if event == self.trigger:
            self.run(event)
    @abstractmethod
    def run(self,event) -> Iterable[ControlPolicy]:
        pass
'''
