#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import logging
from typing import Any, Dict, List

from graphene import Schema

from silvaengine_dynamodb_base import SilvaEngineDynamoDBBase

from .handlers.config import Config
from .handlers.inquiry import InquiryHandler
from .handlers.modification import ModificationHandler
from .schema import Mutations, Query, type_class


# Hook function applied to deployment
def deploy() -> List:
    return [
        {
            "service": "DTM Core",
            "class": "DTMCoreEngine",
            "functions": {
                "dtm_core_graphql": {
                    "is_static": False,
                    "label": "DTM Core GraphQL",
                    "query": [
                        {"action": "ping", "label": "Ping"},
                        {"action": "module", "label": "View Module"},
                        {"action": "moduleList", "label": "View Module List"},
                        {"action": "dataSource", "label": "View Data Source"},
                        {"action": "dataSourceList", "label": "View Data Source List"},
                        {"action": "model", "label": "View Model"},
                        {"action": "modelList", "label": "View Model List"},
                        {"action": "associatedModel", "label": "View Associated Model"},
                        {
                            "action": "associatedModelList",
                            "label": "View Associated Model List",
                        },
                        {"action": "modelAction", "label": "View Model Action"},
                        {
                            "action": "modelActionList",
                            "label": "View Model Action List",
                        },
                        {
                            "action": "associatedModelAction",
                            "label": "View Associated Model Action",
                        },
                        {
                            "action": "associatedModelActionList",
                            "label": "View Associated Model Action List",
                        },
                        {
                            "action": "modelActionTx",
                            "label": "View Model Action Transaction",
                        },
                        {
                            "action": "modelActionTxList",
                            "label": "View Model Action Transaction List",
                        },
                        {
                            "action": "primaryKeyMeta",
                            "label": "View Primary Key Metadata",
                        },
                        {
                            "action": "primaryKeyMetaList",
                            "label": "View Primary Key Metadata List",
                        },
                    ],
                    "mutation": [
                        {
                            "action": "insertUpdateModule",
                            "label": "Create Update Module",
                        },
                        {"action": "deleteModule", "label": "Delete Module"},
                        {
                            "action": "insertUpdateDataSource",
                            "label": "Create Update Data Source",
                        },
                        {"action": "deleteDataSource", "label": "Delete Data Source"},
                        {"action": "insertUpdateModel", "label": "Create Update Model"},
                        {"action": "deleteModel", "label": "Delete Model"},
                        {
                            "action": "insertUpdateAssociatedModel",
                            "label": "Create Update Associated Model",
                        },
                        {
                            "action": "deleteAssociatedModel",
                            "label": "Delete Associated Model",
                        },
                        {
                            "action": "insertUpdateModelAction",
                            "label": "Create Update Model Action",
                        },
                        {"action": "deleteModelAction", "label": "Delete Model Action"},
                        {
                            "action": "insertUpdateAssociatedModelAction",
                            "label": "Create Update Associated Model Action",
                        },
                        {
                            "action": "deleteAssociatedModelAction",
                            "label": "Delete Associated Model Action",
                        },
                        {
                            "action": "insertUpdateModelActionTx",
                            "label": "Create Update Model Action Transaction",
                        },
                        {
                            "action": "deleteModelActionTx",
                            "label": "Delete Model Action Transaction",
                        },
                        {
                            "action": "insertUpdatePrimaryKeyMeta",
                            "label": "Create Update Primary Key Metadata",
                        },
                        {
                            "action": "deletePrimaryKeyMeta",
                            "label": "Delete Primary Key Metadata",
                        },
                    ],
                    "type": "RequestResponse",
                    "support_methods": ["POST"],
                    "is_auth_required": False,
                    "is_graphql": True,
                    "settings": "dtm_core",
                    "disabled_in_resources": True,  # Ignore adding to resource list.
                },
                "dtm_core_inquiry": {
                    "is_static": False,
                    "label": "DTM Core Inquiry Direct",
                    "type": "RequestResponse",
                    "support_methods": ["POST"],
                    "is_auth_required": False,
                    "is_graphql": False,
                    "settings": "dtm_core",
                },
                "dtm_core_modification": {
                    "is_static": False,
                    "label": "DTM Core Modification Direct",
                    "type": "RequestResponse",
                    "support_methods": ["POST"],
                    "is_auth_required": False,
                    "is_graphql": False,
                    "settings": "dtm_core",
                },
            },
        }
    ]


class DTMCoreEngine(SilvaEngineDynamoDBBase):
    def __init__(self, logger: logging.Logger, **setting: Dict[str, Any]) -> None:
        SilvaEngineDynamoDBBase.__init__(self, logger, **setting)

        # Initialize configuration via the Config class
        Config.initialize(logger, **setting)

        self.logger = logger
        self.setting = setting
        self.endpoint_id = setting.get("endpoint_id")

    def dtm_core_graphql(self, **params: Dict[str, Any]) -> Any:
        ## Test the waters 🧪 before diving in!
        ##<--Testing Data-->##
        if params.get("endpoint_id") is None:
            params["endpoint_id"] = self.setting.get("endpoint_id")
        ##<--Testing Data-->##

        schema = Schema(
            query=Query,
            mutation=Mutations,
            types=type_class(),
        )
        return self.graphql_execute(schema, **params)

    # Unified inquiry function
    def dtm_core_inquiry(self, **params: Dict[str, Any]) -> Any:
        endpoint_id = params.get("endpoint_id") or self.endpoint_id
        action = params.get("action")
        attributes = params.get("attributes")

        if action == "get_module":
            return InquiryHandler.get_module(
                endpoint_id,
                attributes.get("module_uuid"),
                attributes.get("module_name"),
            )
        elif action == "list_modules":
            return InquiryHandler.list_modules(
                endpoint_id, attributes.get("module_name"), attributes.get("limit")
            )
        elif action == "get_data_source":
            return InquiryHandler.get_data_source(
                endpoint_id,
                attributes.get("data_source_uuid"),
                attributes.get("data_source_name"),
            )
        elif action == "list_data_sources":
            return InquiryHandler.list_data_sources(
                endpoint_id, attributes.get("data_source_name"), attributes.get("limit")
            )
        elif action == "get_model":
            return InquiryHandler.get_model(
                endpoint_id,
                attributes.get("model_uuid"),
                attributes.get("model_name"),
                attributes.get("module_uuid"),
            )
        elif action == "list_models":
            return InquiryHandler.list_models(
                endpoint_id,
                attributes.get("model_name"),
                attributes.get("module_uuid"),
                attributes.get("limit"),
            )
        elif action == "get_model_action":
            return InquiryHandler.get_model_action(
                endpoint_id,
                attributes.get("model_action_uuid"),
                attributes.get("model_action_name"),
                attributes.get("model_uuid"),
            )
        elif action == "list_model_actions":
            return InquiryHandler.list_model_actions(
                endpoint_id,
                attributes.get("model_action_name"),
                attributes.get("model_uuid"),
                attributes.get("limit"),
            )
        elif action == "get_primary_key_meta":
            return InquiryHandler.get_primary_key_meta(
                endpoint_id, params["primary_key_meta_uuid"]
            )
        elif action == "list_primary_key_metas":
            return InquiryHandler.list_primary_key_metas(
                endpoint_id, attributes.get("limit")
            )
        elif action == "get_associated_model":
            return InquiryHandler.get_associated_model(
                endpoint_id,
                attributes.get("associated_model_uuid"),
                attributes.get("model_uuid"),
                attributes.get("action_name_contains"),
            )
        elif action == "list_associated_models":
            return InquiryHandler.list_associated_models(
                endpoint_id,
                attributes.get("model_uuid"),
                attributes.get("action_name_contains"),
                attributes.get("limit"),
            )
        elif action == "get_associated_model_action":
            return InquiryHandler.get_associated_model_action(
                attributes.get("transaction_uuid"),
                attributes.get("status"),
                attributes.get("action_name"),
            )
        elif action == "list_associated_model_actions":
            return InquiryHandler.list_associated_model_actions(
                attributes.get("transaction_uuid"),
                attributes.get("status"),
                attributes.get("action_name"),
                attributes.get("limit"),
            )
        elif action == "get_model_action_tx":
            return InquiryHandler.get_model_action_tx(
                endpoint_id,
                attributes.get("model_action_uuid"),
                attributes.get("transaction_uuid"),
                attributes.get("status"),
            )
        elif action == "list_model_action_txs":
            return InquiryHandler.list_model_action_txs(
                endpoint_id,
                attributes.get("model_action_uuid"),
                attributes.get("status"),
                attributes.get("limit"),
            )
        else:
            raise ValueError(f"Unknown action: {action}")

    # Unified modification function
    def dtm_core_modification(self, **params: Dict[str, Any]) -> Any:
        endpoint_id = params.get("endpoint_id") or self.endpoint_id
        action = params.get("action")
        attributes = params.get("attributes")

        if action == "insert_update_module":
            return ModificationHandler.insert_update_module(endpoint_id, **attributes)
        elif action == "insert_update_data_source":
            return ModificationHandler.insert_update_data_source(endpoint_id, **attributes)
        elif action == "insert_update_model":
            return ModificationHandler.insert_update_model(endpoint_id, **attributes)
        elif action == "insert_update_model_action":
            return ModificationHandler.insert_update_model_action(
                endpoint_id, **attributes
            )
        elif action == "insert_update_primary_key_meta":
            return ModificationHandler.insert_update_primary_key_meta(
                endpoint_id, **attributes
            )
        elif action == "insert_update_associated_model":
            return ModificationHandler.insert_update_associated_model(
                endpoint_id, **attributes
            )
        elif action == "insert_update_associated_model_action":
            return ModificationHandler.insert_update_associated_model_action(
                endpoint_id, **attributes
            )
        elif action == "insert_update_model_action_tx":
            return ModificationHandler.insert_update_model_action_tx(
                endpoint_id, **attributes
            )
        elif action == "delete_module":
            return ModificationHandler.delete_module(endpoint_id, **attributes)
        elif action == "delete_data_source":
            return ModificationHandler.delete_data_source(endpoint_id, **attributes)
        elif action == "delete_model":
            return ModificationHandler.delete_model(endpoint_id, **attributes)
        elif action == "delete_model_action":
            return ModificationHandler.delete_model_action(endpoint_id, **attributes)
        elif action == "delete_primary_key_meta":
            return ModificationHandler.delete_primary_key_meta(endpoint_id, **attributes)
        elif action == "delete_associated_model":
            return ModificationHandler.delete_associated_model(endpoint_id, **attributes)
        elif action == "delete_associated_model_action":
            return ModificationHandler.delete_associated_model_action(endpoint_id, **attributes)
        elif action == "delete_model_action_tx":
            return ModificationHandler.delete_model_action_tx(endpoint_id, **attributes)
        else:
            raise ValueError(f"Unknown action: {action}")
