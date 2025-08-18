# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import traceback
from typing import Any, Dict

from graphene import Boolean, Field, Mutation, String

from ..models.module import delete_module, insert_update_module
from ..types.module import ModuleType


class InsertUpdateModule(Mutation):
    module = Field(ModuleType)

    class Arguments:
        module_uuid = String(required=True)
        module_name = String(required=False)
        class_name = String(required=False)
        package_name = String(required=False)
        data_source_uuid = String(required=False)
        source = String(required=False)
        updated_by = String(required=True)

    @staticmethod
    def mutate(root: Any, info: Any, **kwargs: Dict[str, Any]) -> "InsertUpdateModule":
        try:
            module = insert_update_module(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return InsertUpdateModule(module=module)


class DeleteModule(Mutation):
    ok = Boolean()

    class Arguments:
        module_uuid = String(required=True)

    @staticmethod
    def mutate(root: Any, info: Any, **kwargs: Dict[str, Any]) -> "DeleteModule":
        try:
            ok = delete_module(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return DeleteModule(ok=ok)
