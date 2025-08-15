#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict

from graphene import ResolveInfo

from ..models import model_action
from ..types.model_action import ModelActionListType, ModelActionType


def resolve_model_action(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> ModelActionType:
    return model_action.resolve_model_action(info, **kwargs)


def resolve_model_action_list(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> ModelActionListType:
    return model_action.resolve_model_action_list(info, **kwargs)
