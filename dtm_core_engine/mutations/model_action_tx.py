# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import traceback
from typing import Any, Dict

from graphene import Boolean, Field, Mutation, String

from silvaengine_utility import JSON

from ..models.model_action_tx import (
    delete_model_action_tx,
    insert_update_model_action_tx,
)
from ..types.model_action_tx import ModelActionTxType


class InsertUpdateModelActionTx(Mutation):
    model_action_tx = Field(ModelActionTxType)

    class Arguments:
        model_action_uuid = String(required=True)
        transaction_uuid = String(required=True)
        associated_model_uuid = String(required=True)
        primary_key = JSON(required=False)
        arguments = JSON(required=False)
        status = String(required=False)
        notes = String(required=False)

    @staticmethod
    def mutate(
        root: Any, info: Any, **kwargs: Dict[str, Any]
    ) -> "InsertUpdateModelActionTx":
        try:
            model_action_tx = insert_update_model_action_tx(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return InsertUpdateModelActionTx(model_action_tx=model_action_tx)


class DeleteModelActionTx(Mutation):
    ok = Boolean()

    class Arguments:
        model_action_uuid = String(required=True)
        transaction_uuid = String(required=True)

    @staticmethod
    def mutate(root: Any, info: Any, **kwargs: Dict[str, Any]) -> "DeleteModelActionTx":
        try:
            ok = delete_model_action_tx(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return DeleteModelActionTx(ok=ok)
