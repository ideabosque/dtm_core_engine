#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import logging
from typing import Any, Dict, List

from graphene import Schema

from silvaengine_dynamodb_base import SilvaEngineDynamoDBBase
from silvaengine_utility import Utility

from .handlers.config import Config
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
