#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import time
from typing import Any, Dict

from graphene import Field, Int, ObjectType, ResolveInfo, String

from .mutations.associated_model import (
    DeleteAssociatedModel,
    InsertUpdateAssociatedModel,
)
from .mutations.associated_model_action import (
    DeleteAssociatedModelAction,
    InsertUpdateAssociatedModelAction,
)
from .mutations.model import DeleteModel, InsertUpdateModel
from .mutations.model_action import DeleteModelAction, InsertUpdateModelAction
from .mutations.model_action_tx import DeleteModelActionTx, InsertUpdateModelActionTx
from .mutations.module import DeleteModule, InsertUpdateModule
from .mutations.data_source import DeleteDataSource, InsertUpdateDataSource
from .mutations.primary_key_meta import DeletePrimaryKeyMeta, InsertUpdatePrimaryKeyMeta
from .queries.associated_model import (
    resolve_associated_model,
    resolve_associated_model_list,
)
from .queries.associated_model_action import (
    resolve_associated_model_action,
    resolve_associated_model_action_list,
)
from .queries.model import resolve_model, resolve_model_list
from .queries.model_action import resolve_model_action, resolve_model_action_list
from .queries.model_action_tx import (
    resolve_model_action_tx,
    resolve_model_action_tx_list,
)
from .queries.module import resolve_module, resolve_module_list
from .queries.data_source import resolve_data_source, resolve_data_source_list
from .queries.primary_key_meta import (
    resolve_primary_key_meta,
    resolve_primary_key_meta_list,
)
from .types.associated_model import AssociatedModelListType, AssociatedModelType
from .types.associated_model_action import (
    AssociatedModelActionListType,
    AssociatedModelActionType,
)
from .types.model import ModelListType, ModelType
from .types.model_action import ModelActionListType, ModelActionType
from .types.model_action_tx import ModelActionTxListType, ModelActionTxType
from .types.module import ModuleListType, ModuleType
from .types.data_source import DataSourceListType, DataSourceType
from .types.primary_key_meta import PrimaryKeyMetaListType, PrimaryKeyMetaType


def type_class():
    return [
        ModuleType,
        ModuleListType,
        DataSourceType,
        DataSourceListType,
        ModelType,
        ModelListType,
        AssociatedModelType,
        AssociatedModelListType,
        ModelActionType,
        ModelActionListType,
        AssociatedModelActionType,
        AssociatedModelActionListType,
        ModelActionTxType,
        ModelActionTxListType,
        PrimaryKeyMetaType,
        PrimaryKeyMetaListType,
    ]


class Query(ObjectType):
    ping = String()

    module = Field(
        ModuleType,
        module_uuid=String(required=False),
        module_name=String(required=False),
    )

    module_list = Field(
        ModuleListType,
        page_number=Int(required=False),
        limit=Int(required=False),
        module_name=String(required=False),
    )

    data_source = Field(
        DataSourceType,
        data_source_uuid=String(required=False),
        data_source_name=String(required=False),
    )

    data_source_list = Field(
        DataSourceListType,
        page_number=Int(required=False),
        limit=Int(required=False),
        data_source_name=String(required=False),
    )

    model = Field(
        ModelType,
        module_uuid=String(required=True),
        model_uuid=String(required=False),
        model_name=String(required=False),
    )

    model_list = Field(
        ModelListType,
        page_number=Int(required=False),
        limit=Int(required=False),
        module_uuid=String(required=False),
        model_name=String(required=False),
    )

    associated_model = Field(
        AssociatedModelType,
        associated_model_uuid=String(required=True),
    )

    associated_model_list = Field(
        AssociatedModelListType,
        page_number=Int(required=False),
        limit=Int(required=False),
        model_uuid=String(required=False),
        action_name_contains=String(required=False),
    )

    model_action = Field(
        ModelActionType,
        model_action_uuid=String(required=True),
    )

    model_action_list = Field(
        ModelActionListType,
        page_number=Int(required=False),
        limit=Int(required=False),
        model_uuid=String(required=False),
        action_name=String(required=False),
    )

    associated_model_action = Field(
        AssociatedModelActionType,
        transaction_uuid=String(required=True),
        action_name=String(required=True),
    )

    associated_model_action_list = Field(
        AssociatedModelActionListType,
        page_number=Int(required=False),
        limit=Int(required=False),
        transaction_uuid=String(required=False),
        status=String(required=False),
        action_name=String(required=False),
    )

    model_action_tx = Field(
        ModelActionTxType,
        model_action_uuid=String(required=True),
        transaction_uuid=String(required=True),
    )

    model_action_tx_list = Field(
        ModelActionTxListType,
        page_number=Int(required=False),
        limit=Int(required=False),
        model_action_uuid=String(required=False),
        status=String(required=False),
    )

    primary_key_meta = Field(
        PrimaryKeyMetaType,
        associated_model_uuid=String(required=True),
        primary_key_metadata_uuid=String(required=True),
    )

    primary_key_meta_list = Field(
        PrimaryKeyMetaListType,
        page_number=Int(required=False),
        limit=Int(required=False),
        associated_model_uuid=String(required=False),
        attribute_name=String(required=False),
    )

    def resolve_ping(self, info: ResolveInfo) -> str:
        return f"DTM Core Engine - Hello at {time.strftime('%X')}!!"

    def resolve_module(self, info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModuleType:
        return resolve_module(info, **kwargs)

    def resolve_module_list(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> ModuleListType:
        return resolve_module_list(info, **kwargs)

    def resolve_data_source(self, info: ResolveInfo, **kwargs: Dict[str, Any]) -> DataSourceType:
        return resolve_data_source(info, **kwargs)

    def resolve_data_source_list(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> DataSourceListType:
        return resolve_data_source_list(info, **kwargs)

    def resolve_model(self, info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModelType:
        return resolve_model(info, **kwargs)

    def resolve_model_list(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> ModelListType:
        return resolve_model_list(info, **kwargs)

    def resolve_associated_model(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> AssociatedModelType:
        return resolve_associated_model(info, **kwargs)

    def resolve_associated_model_list(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> AssociatedModelListType:
        return resolve_associated_model_list(info, **kwargs)

    def resolve_model_action(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> ModelActionType:
        return resolve_model_action(info, **kwargs)

    def resolve_model_action_list(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> ModelActionListType:
        return resolve_model_action_list(info, **kwargs)

    def resolve_associated_model_action(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> AssociatedModelActionType:
        return resolve_associated_model_action(info, **kwargs)

    def resolve_associated_model_action_list(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> AssociatedModelActionListType:
        return resolve_associated_model_action_list(info, **kwargs)

    def resolve_model_action_tx(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> ModelActionTxType:
        return resolve_model_action_tx(info, **kwargs)

    def resolve_model_action_tx_list(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> ModelActionTxListType:
        return resolve_model_action_tx_list(info, **kwargs)

    def resolve_primary_key_meta(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> PrimaryKeyMetaType:
        return resolve_primary_key_meta(info, **kwargs)

    def resolve_primary_key_meta_list(
        self, info: ResolveInfo, **kwargs: Dict[str, Any]
    ) -> PrimaryKeyMetaListType:
        return resolve_primary_key_meta_list(info, **kwargs)


class Mutations(ObjectType):
    insert_update_module = InsertUpdateModule.Field()
    delete_module = DeleteModule.Field()
    insert_update_data_source = InsertUpdateDataSource.Field()
    delete_data_source = DeleteDataSource.Field()
    insert_update_model = InsertUpdateModel.Field()
    delete_model = DeleteModel.Field()
    insert_update_associated_model = InsertUpdateAssociatedModel.Field()
    delete_associated_model = DeleteAssociatedModel.Field()
    insert_update_model_action = InsertUpdateModelAction.Field()
    delete_model_action = DeleteModelAction.Field()
    insert_update_associated_model_action = InsertUpdateAssociatedModelAction.Field()
    delete_associated_model_action = DeleteAssociatedModelAction.Field()
    insert_update_model_action_tx = InsertUpdateModelActionTx.Field()
    delete_model_action_tx = DeleteModelActionTx.Field()
    insert_update_primary_key_meta = InsertUpdatePrimaryKeyMeta.Field()
    delete_primary_key_meta = DeletePrimaryKeyMeta.Field()
