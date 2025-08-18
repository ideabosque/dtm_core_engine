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
    def insert_update_data_source(
        endpoint_id: str, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:

        from ..models.data_source import insert_update_data_source

        info.context = {"endpoint_id": endpoint_id}
        result = insert_update_data_source(info, **kwargs)
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

    @staticmethod
    def delete_module(endpoint_id: str, **kwargs: Dict[str, Any]) -> bool:
        from ..models.module import delete_module
        info.context = {"endpoint_id": endpoint_id}
        return delete_module(info, **kwargs)

    @staticmethod
    def delete_data_source(endpoint_id: str, **kwargs: Dict[str, Any]) -> bool:
        from ..models.data_source import delete_data_source
        info.context = {"endpoint_id": endpoint_id}
        return delete_data_source(info, **kwargs)

    @staticmethod
    def delete_model(endpoint_id: str, **kwargs: Dict[str, Any]) -> bool:
        from ..models.model import delete_model
        info.context = {"endpoint_id": endpoint_id}
        return delete_model(info, **kwargs)

    @staticmethod
    def delete_model_action(endpoint_id: str, **kwargs: Dict[str, Any]) -> bool:
        from ..models.model_action import delete_model_action
        info.context = {"endpoint_id": endpoint_id}
        return delete_model_action(info, **kwargs)

    @staticmethod
    def delete_primary_key_meta(endpoint_id: str, **kwargs: Dict[str, Any]) -> bool:
        from ..models.primary_key_meta import delete_primary_key_meta
        info.context = {"endpoint_id": endpoint_id}
        return delete_primary_key_meta(info, **kwargs)

    @staticmethod
    def delete_associated_model(endpoint_id: str, **kwargs: Dict[str, Any]) -> bool:
        from ..models.associated_model import delete_associated_model
        info.context = {"endpoint_id": endpoint_id}
        return delete_associated_model(info, **kwargs)

    @staticmethod
    def delete_associated_model_action(endpoint_id: str, **kwargs: Dict[str, Any]) -> bool:
        from ..models.associated_model_action import delete_associated_model_action
        info.context = {"endpoint_id": endpoint_id}
        return delete_associated_model_action(info, **kwargs)

    @staticmethod
    def delete_model_action_tx(endpoint_id: str, **kwargs: Dict[str, Any]) -> bool:
        from ..models.model_action_tx import delete_model_action_tx
        info.context = {"endpoint_id": endpoint_id}
        return delete_model_action_tx(info, **kwargs)
