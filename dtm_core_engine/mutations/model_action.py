# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import traceback
from typing import Any, Dict

from graphene import Boolean, Field, List, Mutation, String

from ..models.model_action import delete_model_action, insert_update_model_action
from ..types.model_action import ModelActionType


class InsertUpdateModelAction(Mutation):
    model_action = Field(ModelActionType)

    class Arguments:
        model_action_uuid = String(required=True)
        model_uuid = String(required=True)
        action_name = String(required=True)
        associated_model_uuids = List(String, required=False)

    @staticmethod
    def mutate(
        root: Any, info: Any, **kwargs: Dict[str, Any]
    ) -> "InsertUpdateModelAction":
        try:
            model_action = insert_update_model_action(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return InsertUpdateModelAction(model_action=model_action)


class DeleteModelAction(Mutation):
    ok = Boolean()

    class Arguments:
        model_action_uuid = String(required=True)

    @staticmethod
    def mutate(root: Any, info: Any, **kwargs: Dict[str, Any]) -> "DeleteModelAction":
        try:
            ok = delete_model_action(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return DeleteModelAction(ok=ok)
