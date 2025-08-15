# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import traceback
from typing import Any, Dict

from graphene import Boolean, Field, Mutation, String

from ..models.model import delete_model, insert_update_model
from ..types.model import ModelType


class InsertUpdateModel(Mutation):
    model = Field(ModelType)

    class Arguments:
        module_uuid = String(required=True)
        model_uuid = String(required=True)
        model_name = String(required=False)

    @staticmethod
    def mutate(root: Any, info: Any, **kwargs: Dict[str, Any]) -> "InsertUpdateModel":
        try:
            model = insert_update_model(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return InsertUpdateModel(model=model)


class DeleteModel(Mutation):
    ok = Boolean()

    class Arguments:
        module_uuid = String(required=True)
        model_uuid = String(required=True)

    @staticmethod
    def mutate(root: Any, info: Any, **kwargs: Dict[str, Any]) -> "DeleteModel":
        try:
            ok = delete_model(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return DeleteModel(ok=ok)
