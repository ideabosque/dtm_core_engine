# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import traceback
from typing import Any, Dict

from graphene import Boolean, Field, Mutation, String

from silvaengine_utility import JSON

from ..models.associated_model_action import (
    delete_associated_model_action,
    insert_update_associated_model_action,
)
from ..types.associated_model_action import AssociatedModelActionType


class InsertUpdateAssociatedModelAction(Mutation):
    associated_model_action = Field(AssociatedModelActionType)

    class Arguments:
        transaction_uuid = String(required=True)
        action_name = String(required=True)
        model_action_uuid = String(required=True)
        status = String(required=False)
        response = JSON(required=False)
        notes = String(required=False)

    @staticmethod
    def mutate(
        root: Any, info: Any, **kwargs: Dict[str, Any]
    ) -> "InsertUpdateAssociatedModelAction":
        try:
            associated_model_action = insert_update_associated_model_action(
                info, **kwargs
            )
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return InsertUpdateAssociatedModelAction(
            associated_model_action=associated_model_action
        )


class DeleteAssociatedModelAction(Mutation):
    ok = Boolean()

    class Arguments:
        transaction_uuid = String(required=True)
        action_name = String(required=True)

    @staticmethod
    def mutate(
        root: Any, info: Any, **kwargs: Dict[str, Any]
    ) -> "DeleteAssociatedModelAction":
        try:
            ok = delete_associated_model_action(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return DeleteAssociatedModelAction(ok=ok)
