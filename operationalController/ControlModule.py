# -*- coding: utf-8 -*-
from typing import List, Dict, Any, Union, Iterable
from abc import ABC, abstractmethod
from .ControlPolicy import ControlPolicy

class ControlModule:
    target:Dict[str,Iterable[Any]]
    def __call__(self,*args,**kwargs):
        pass