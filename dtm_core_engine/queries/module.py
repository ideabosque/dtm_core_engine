#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict

from graphene import ResolveInfo

from ..models import module
from ..types.module import ModuleListType, ModuleType


def resolve_module(info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModuleType:
    return module.resolve_module(info, **kwargs)


def resolve_module_list(info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModuleListType:
    return module.resolve_module_list(info, **kwargs)
