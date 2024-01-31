# -*- coding: utf-8 -*-
from typing import List, Dict, Any, Union, Iterable
from abc import ABC, abstractmethod
from .controlPolicy import ControlPolicy

class ControlModule:
    target:Dict[str,Iterable[Any]]
    inputParameters:List[str] = list()
    _controller = None
    def __call__(self,*args,**kwargs):
        return self.run(*args,**kwargs)
    @abstractmethod
    def solve(self,*args,**kwargs) -> Iterable:
        return []
    def getInputParamters(self):
        return self.inputParameters
