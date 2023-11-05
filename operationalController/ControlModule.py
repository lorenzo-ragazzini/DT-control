# -*- coding: utf-8 -*-
from typing import List, Dict, Any, Union, Iterable
from abc import ABC, abstractmethod
from .controlPolicy import ControlPolicy

class ControlModule:
    target:Dict[str,Iterable[Any]]
    _controller = None
    def __init__(self,controller=None):
        self.controller = controller 
    def __call__(self,*args,**kwargs):
        pass