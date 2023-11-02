from typing import List, Dict, Any, Union, Iterable
from abc import ABC, abstractmethod
from .ControlRule import ControlRule

class ControlMap(ABC):
    rules:Dict[str,ControlRule]
    def __call__(self,event):
        for key in self.rules.keys():
            self.rules[key](event)