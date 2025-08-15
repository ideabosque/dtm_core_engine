# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import traceback
from typing import Any, Dict

from graphene import Boolean, Field, Mutation, String

from ..models.primary_key_meta import (
    delete_primary_key_meta,
    insert_update_primary_key_meta,
)
from ..types.primary_key_meta import PrimaryKeyMetaType


class InsertUpdatePrimaryKeyMeta(Mutation):
    primary_key_meta = Field(PrimaryKeyMetaType)

    class Arguments:
        associated_model_uuid = String(required=True)
        primary_key_metadata_uuid = String(required=True)
        attribute_name = String(required=False)
        data_type = String(required=False)
        key_type = String(required=False)

    @staticmethod
    def mutate(
        root: Any, info: Any, **kwargs: Dict[str, Any]
    ) -> "InsertUpdatePrimaryKeyMeta":
        try:
            primary_key_meta = insert_update_primary_key_meta(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return InsertUpdatePrimaryKeyMeta(primary_key_meta=primary_key_meta)


class DeletePrimaryKeyMeta(Mutation):
    ok = Boolean()

    class Arguments:
        associated_model_uuid = String(required=True)
        primary_key_metadata_uuid = String(required=True)

    @staticmethod
    def mutate(
        root: Any, info: Any, **kwargs: Dict[str, Any]
    ) -> "DeletePrimaryKeyMeta":
        try:
            ok = delete_primary_key_meta(info, **kwargs)
        except Exception as e:
            log = traceback.format_exc()
            info.context.get("logger").error(log)
            raise e

        return DeletePrimaryKeyMeta(ok=ok)
