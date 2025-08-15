#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict

from graphene import ResolveInfo

from ..models import model_action_tx
from ..types.model_action_tx import ModelActionTxListType, ModelActionTxType


def resolve_model_action_tx(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> ModelActionTxType:
    return model_action_tx.resolve_model_action_tx(info, **kwargs)


def resolve_model_action_tx_list(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> ModelActionTxListType:
    return model_action_tx.resolve_model_action_tx_list(info, **kwargs)
