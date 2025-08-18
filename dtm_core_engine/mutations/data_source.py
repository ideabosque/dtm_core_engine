# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import traceback
from typing import Any, Dict

from graphene import Boolean, Field, Mutation, String

from silvaengine_utility import JSON

from ..models.data_source import delete_data_source, insert_update_data_source
from ..types.data_source import DataSourceType


class InsertUpdateDataSource(Mutation):
    data_source = Field(DataSourceType)

    class Arguments:
        data_source_uuid = String(required=True)
        data_source_name = String(required=False)
        setting = JSON(required=False)
        connector_class_name = String(required=False)
        connector_module_name = String(required=False)
        updated_by = String(required=True)

    @staticmethod
    def mutate(
        root: Any, info: Any, **kwargs: Dict[str, Any]
    ) -> "InsertUpdateDataSource":
        try:
            data_source = insert_update_data_source(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return InsertUpdateDataSource(data_source=data_source)


class DeleteDataSource(Mutation):
    ok = Boolean()

    class Arguments:
        data_source_uuid = String(required=True)

    @staticmethod
    def mutate(root: Any, info: Any, **kwargs: Dict[str, Any]) -> "DeleteDataSource":
        try:
            ok = delete_data_source(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return DeleteDataSource(ok=ok)
