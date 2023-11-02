from typing import List, Dict, Any, Union, Iterable
from abc import ABC, abstractmethod
from .ControlPolicy import ControlPolicy
from .ControlModule import ControlModule

class ControlRule:
    trigger:None
    target:Dict[str,Iterable[Union[ControlPolicy,ControlModule]]]
    def __call__(self,event) -> Iterable[ControlPolicy]:
        if event == self.trigger:
            self.run(event)
    @abstractmethod
    def run(self) -> Iterable[ControlPolicy]:
        pass