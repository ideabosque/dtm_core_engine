# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import traceback
from typing import Any, Dict

from graphene import Boolean, Field, Mutation, String

from silvaengine_utility import JSON

from ..models.associated_model import (
    delete_associated_model,
    insert_update_associated_model,
)
from ..types.associated_model import AssociatedModelType


class InsertUpdateAssociatedModel(Mutation):
    associated_model = Field(AssociatedModelType)

    class Arguments:
        associated_model_uuid = String(required=True)
        model_uuid = String(required=True)
        actions = JSON(required=False)

    @staticmethod
    def mutate(
        root: Any, info: Any, **kwargs: Dict[str, Any]
    ) -> "InsertUpdateAssociatedModel":
        try:
            associated_model = insert_update_associated_model(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return InsertUpdateAssociatedModel(associated_model=associated_model)


class DeleteAssociatedModel(Mutation):
    ok = Boolean()

    class Arguments:
        associated_model_uuid = String(required=True)
        model_uuid = String(required=True)

    @staticmethod
    def mutate(
        root: Any, info: Any, **kwargs: Dict[str, Any]
    ) -> "DeleteAssociatedModel":
        try:
            ok = delete_associated_model(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return DeleteAssociatedModel(ok=ok)
