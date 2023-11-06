from typing import List, Dict, Any, Union, Iterable
from abc import ABC, abstractmethod
from .controlRule import ControlRule

class ControlMap(ABC):
    rules:List[ControlRule]
    def __call__(self,event):
        policies = []
        for rule in self.rules:
            policies += rule(event)
        return policies
'''
class ControlMap(ABC):
    rules:Dict[str,ControlRule]
    def __call__(self,event):
        for key in self.rules:
            self.rules[key](event)
'''