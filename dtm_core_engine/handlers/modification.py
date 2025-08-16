#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict

from graphene import ResolveInfo

info = ResolveInfo(
    field_name=None,
    field_asts=[],
    return_type=None,
    parent_type=None,
    schema=None,
    fragments={},
    root_value=None,
    operation=None,
    variable_values={},
    context={},
    path=None,
)


class ModificationHandler:
    @staticmethod
    def insert_update_module(
        endpoint_id: str, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:

        from ..models.module import insert_update_module

        info.context = {"endpoint_id": endpoint_id}
        result = insert_update_module(info, **kwargs)
        return result.__dict__ if hasattr(result, "__dict__") else result

    @staticmethod
    def insert_update_model(
        endpoint_id: str, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:

        from ..models.model import insert_update_model

        info.context = {"endpoint_id": endpoint_id}
        result = insert_update_model(info, **kwargs)
        return result.__dict__ if hasattr(result, "__dict__") else result

    @staticmethod
    def insert_update_model_action(
        endpoint_id: str, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:

        from ..models.model_action import insert_update_model_action

        info.context = {"endpoint_id": endpoint_id}
        result = insert_update_model_action(info, **kwargs)
        return result.__dict__ if hasattr(result, "__dict__") else result

    @staticmethod
    def insert_update_primary_key_meta(
        endpoint_id: str, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:

        from ..models.primary_key_meta import insert_update_primary_key_meta

        info.context = {"endpoint_id": endpoint_id}
        result = insert_update_primary_key_meta(info, **kwargs)
        return result.__dict__ if hasattr(result, "__dict__") else result

    @staticmethod
    def insert_update_associated_model(
        endpoint_id: str, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:

        from ..models.associated_model import insert_update_associated_model

        info.context = {"endpoint_id": endpoint_id}
        result = insert_update_associated_model(info, **kwargs)
        return result.__dict__ if hasattr(result, "__dict__") else result

    @staticmethod
    def insert_update_associated_model_action(
        endpoint_id: str, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:

        from ..models.associated_model_action import (
            insert_update_associated_model_action,
        )

        info.context = {"endpoint_id": endpoint_id}
        result = insert_update_associated_model_action(info, **kwargs)
        return result.__dict__ if hasattr(result, "__dict__") else result

    @staticmethod
    def insert_update_model_action_tx(
        endpoint_id: str, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:

        from ..models.model_action_tx import insert_update_model_action_tx

        info.context = {"endpoint_id": endpoint_id}
        result = insert_update_model_action_tx(info, **kwargs)
        return result.__dict__ if hasattr(result, "__dict__") else result
