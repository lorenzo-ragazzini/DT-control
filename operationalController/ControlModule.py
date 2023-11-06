# -*- coding: utf-8 -*-
from typing import List, Dict, Any, Union, Iterable
from abc import ABC, abstractmethod
from .controlPolicy import ControlPolicy

class ControlModule:
    target:Dict[str,Iterable[Any]]
    _controller = None
    def __call__(self,*args,**kwargs):
        return self.run(*args,**kwargs)
    @abstractmethod
    def run(self,*args,**kwargs):
        pass