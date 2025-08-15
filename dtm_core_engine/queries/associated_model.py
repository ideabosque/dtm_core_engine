#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict

from graphene import ResolveInfo

from ..models import associated_model
from ..types.associated_model import AssociatedModelListType, AssociatedModelType


def resolve_associated_model(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> AssociatedModelType:
    return associated_model.resolve_associated_model(info, **kwargs)


def resolve_associated_model_list(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> AssociatedModelListType:
    return associated_model.resolve_associated_model_list(info, **kwargs)
