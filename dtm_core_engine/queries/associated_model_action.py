#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict

from graphene import ResolveInfo

from ..models import associated_model_action
from ..types.associated_model_action import (
    AssociatedModelActionListType,
    AssociatedModelActionType,
)


def resolve_associated_model_action(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> AssociatedModelActionType:
    return associated_model_action.resolve_associated_model_action(info, **kwargs)


def resolve_associated_model_action_list(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> AssociatedModelActionListType:
    return associated_model_action.resolve_associated_model_action_list(info, **kwargs)
