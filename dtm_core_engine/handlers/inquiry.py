#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict, List, Optional


class InquiryHandler:
    @staticmethod
    def get_module(
        endpoint_id: str, module_uuid: str = None, module_name: str = None
    ) -> Optional[Dict[str, Any]]:
        from ..models.module import ModuleRepo

        repo = ModuleRepo()
        if module_uuid:
            key = repo.key(endpoint_id, module_uuid)
            return repo.get(key)
        elif module_name:
            modules = repo.list(
                endpoint_id=endpoint_id, module_name=module_name, limit=1
            )
            return modules[0] if modules else None
        return None

    @staticmethod
    def list_modules(
        endpoint_id: str, module_name: str = None, limit: int = None
    ) -> List[Dict[str, Any]]:
        from ..models.module import ModuleRepo

        repo = ModuleRepo()
        return repo.list(endpoint_id=endpoint_id, module_name=module_name, limit=limit)

    @staticmethod
    def get_data_source(
        endpoint_id: str, data_source_uuid: str = None, data_source_name: str = None
    ) -> Optional[Dict[str, Any]]:
        from ..models.data_source import DataSourceRepo

        repo = DataSourceRepo()
        if data_source_uuid:
            key = repo.key(endpoint_id, data_source_uuid)
            return repo.get(key)
        elif data_source_name:
            data_sources = repo.list(
                endpoint_id=endpoint_id, data_source_name=data_source_name, limit=1
            )
            return data_sources[0] if data_sources else None
        return None

    @staticmethod
    def list_data_sources(
        endpoint_id: str, data_source_name: str = None, limit: int = None
    ) -> List[Dict[str, Any]]:
        from ..models.data_source import DataSourceRepo

        repo = DataSourceRepo()
        return repo.list(endpoint_id=endpoint_id, data_source_name=data_source_name, limit=limit)

    @staticmethod
    def get_model(
        endpoint_id: str,
        model_uuid: str = None,
        model_name: str = None,
        module_uuid: str = None,
    ) -> Optional[Dict[str, Any]]:
        from ..models.model import ModelRepo

        repo = ModelRepo()
        if model_uuid and module_uuid:
            key = repo.key(module_uuid, model_uuid)
            return repo.get(key)
        elif model_name:
            models = repo.list(
                endpoint_id=endpoint_id,
                model_name=model_name,
                module_uuid=module_uuid,
                limit=1,
            )
            return models[0] if models else None
        return None

    @staticmethod
    def list_models(
        endpoint_id: str,
        model_name: str = None,
        module_uuid: str = None,
        limit: int = None,
    ) -> List[Dict[str, Any]]:
        from ..models.model import ModelRepo

        repo = ModelRepo()
        return repo.list(
            endpoint_id=endpoint_id,
            model_name=model_name,
            module_uuid=module_uuid,
            limit=limit,
        )

    @staticmethod
    def get_model_action(
        endpoint_id: str,
        model_action_uuid: str = None,
        model_action_name: str = None,
        model_uuid: str = None,
    ) -> Optional[Dict[str, Any]]:
        from ..models.model_action import ModelActionRepo

        repo = ModelActionRepo()
        if model_action_uuid:
            key = repo.key(endpoint_id, model_action_uuid)
            return repo.get(key)
        elif model_action_name:
            actions = repo.list(
                endpoint_id=endpoint_id,
                model_action_name=model_action_name,
                model_uuid=model_uuid,
                limit=1,
            )
            return actions[0] if actions else None
        return None

    @staticmethod
    def list_model_actions(
        endpoint_id: str,
        model_action_name: str = None,
        model_uuid: str = None,
        limit: int = None,
    ) -> List[Dict[str, Any]]:
        from ..models.model_action import ModelActionRepo

        repo = ModelActionRepo()
        return repo.list(
            endpoint_id=endpoint_id,
            model_action_name=model_action_name,
            model_uuid=model_uuid,
            limit=limit,
        )

    @staticmethod
    def get_primary_key_meta(
        endpoint_id: str, primary_key_meta_uuid: str
    ) -> Optional[Dict[str, Any]]:
        from ..models.primary_key_meta import PrimaryKeyMetaRepo

        repo = PrimaryKeyMetaRepo()
        key = repo.key(endpoint_id, primary_key_meta_uuid)
        return repo.get(key)

    @staticmethod
    def list_primary_key_metas(
        endpoint_id: str, limit: int = None
    ) -> List[Dict[str, Any]]:
        from ..models.primary_key_meta import PrimaryKeyMetaRepo

        repo = PrimaryKeyMetaRepo()
        return repo.list(endpoint_id=endpoint_id, limit=limit)

    @staticmethod
    def get_associated_model(
        endpoint_id: str,
        associated_model_uuid: str = None,
        model_uuid: str = None,
        action_name_contains: str = None,
    ) -> Optional[Dict[str, Any]]:
        from ..models.associated_model import AssociatedModelRepo

        repo = AssociatedModelRepo()
        if associated_model_uuid:
            key = repo.key(endpoint_id, associated_model_uuid)
            return repo.get(key)
        else:
            models = repo.list(
                endpoint_id=endpoint_id,
                model_uuid=model_uuid,
                action_name_contains=action_name_contains,
                limit=1,
            )
            return models[0] if models else None

    @staticmethod
    def list_associated_models(
        endpoint_id: str,
        model_uuid: str = None,
        action_name_contains: str = None,
        limit: int = None,
    ) -> List[Dict[str, Any]]:
        from ..models.associated_model import AssociatedModelRepo

        repo = AssociatedModelRepo()
        return repo.list(
            endpoint_id=endpoint_id,
            model_uuid=model_uuid,
            action_name_contains=action_name_contains,
            limit=limit,
        )

    @staticmethod
    def get_associated_model_action(
        transaction_uuid: str = None, status: str = None, action_name: str = None
    ) -> Optional[Dict[str, Any]]:
        from ..models.associated_model_action import AssociatedModelActionRepo

        repo = AssociatedModelActionRepo()
        actions = repo.list(
            transaction_uuid=transaction_uuid,
            status=status,
            action_name=action_name,
            limit=1,
        )
        return actions[0] if actions else None

    @staticmethod
    def list_associated_model_actions(
        transaction_uuid: str = None,
        status: str = None,
        action_name: str = None,
        limit: int = None,
    ) -> List[Dict[str, Any]]:
        from ..models.associated_model_action import AssociatedModelActionRepo

        repo = AssociatedModelActionRepo()
        return repo.list(
            transaction_uuid=transaction_uuid,
            status=status,
            action_name=action_name,
            limit=limit,
        )

    @staticmethod
    def get_model_action_tx(
        endpoint_id: str,
        model_action_uuid: str = None,
        transaction_uuid: str = None,
        status: str = None,
    ) -> Optional[Dict[str, Any]]:
        from ..models.model_action_tx import ModelActionTxRepo

        repo = ModelActionTxRepo()
        if model_action_uuid and transaction_uuid:
            key = repo.key(model_action_uuid, transaction_uuid)
            return repo.get(key)
        else:
            txs = repo.list(
                model_action_uuid=model_action_uuid,
                endpoint_id=endpoint_id,
                status=status,
                limit=1,
            )
            return txs[0] if txs else None

    @staticmethod
    def list_model_action_txs(
        endpoint_id: str,
        model_action_uuid: str = None,
        status: str = None,
        limit: int = None,
    ) -> List[Dict[str, Any]]:
        from ..models.model_action_tx import ModelActionTxRepo

        repo = ModelActionTxRepo()
        return repo.list(
            model_action_uuid=model_action_uuid,
            endpoint_id=endpoint_id,
            status=status,
            limit=limit,
        )
