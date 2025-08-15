#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict

from graphene import ResolveInfo

from ..models import model
from ..types.model import ModelListType, ModelType


def resolve_model(info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModelType:
    return model.resolve_model(info, **kwargs)


def resolve_model_list(info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModelListType:
    return model.resolve_model_list(info, **kwargs)
