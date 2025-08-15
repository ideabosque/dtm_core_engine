# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict, List, Optional, Tuple

import pendulum
from graphene import ResolveInfo

from silvaengine_utility import Utility

from ..handlers import etcd_client
from ..types.model_action_tx import ModelActionTxListType, ModelActionTxType
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_tx(model_action_uuid, transaction_uuid):
    return f"{ETCD_PREFIX}/model_action_tx/{model_action_uuid}/{transaction_uuid}"


class ModelActionTxRepo(BaseRepo):
    def key(self, model_action_uuid: str, transaction_uuid: str) -> str:
        return k_tx(model_action_uuid, transaction_uuid)

    def list(
        self,
        *,
        model_action_uuid: Optional[str] = None,
        endpoint_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        prefix = (
            f"{ETCD_PREFIX}/model_action_tx/{model_action_uuid}/"
            if model_action_uuid
            else f"{ETCD_PREFIX}/model_action_tx/"
        )
        results: List[dict] = []
        for _k, payload in self._iter_prefix(prefix):
            if not payload:
                continue
            if endpoint_id and not match(payload, endpoint_id=endpoint_id):
                continue
            if status and not match(payload, status=status):
                continue
            results.append(payload)
            if limit and len(results) >= limit:
                break
        return results

    def delete_safe(
        self, model_action_uuid: str, transaction_uuid: str
    ) -> Tuple[bool, List[str]]:
        blockers: List[str] = []
        if etcd_client.has_any(
            f"{ETCD_PREFIX}/associated_model_actions/{transaction_uuid}/"
        ):
            blockers.append("Associated model actions exist under this transaction")
        if blockers:
            return False, blockers
        ok = self.delete_key_only(self.key(model_action_uuid, transaction_uuid))
        return ok, ([] if ok else ["Delete failed"])


def resolve_model_action_tx(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> ModelActionTxType:
    repo = ModelActionTxRepo()
    model_action_uuid = kwargs.get("model_action_uuid")
    transaction_uuid = kwargs.get("transaction_uuid")

    if model_action_uuid and transaction_uuid:
        # Direct lookup by UUIDs
        key = repo.key(model_action_uuid, transaction_uuid)
        tx_data = repo.get(key)
        if not tx_data:
            return None
    else:
        # List lookup
        txs = repo.list(
            model_action_uuid=model_action_uuid,
            endpoint_id=info.context["endpoint_id"],
            status=kwargs.get("status"),
            limit=1,
        )
        if not txs:
            return None
        tx_data = txs[0]

    return ModelActionTxType(**repo._process_datetime_fields(tx_data))


def resolve_model_action_tx_list(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> ModelActionTxListType:
    repo = ModelActionTxRepo()
    txs = repo.list(
        model_action_uuid=kwargs.get("model_action_uuid"),
        endpoint_id=info.context["endpoint_id"],
        status=kwargs.get("status"),
        limit=kwargs.get("limit"),
    )
    tx_list = [ModelActionTxType(**repo._process_datetime_fields(t)) for t in txs]
    return ModelActionTxListType(model_action_tx_list=tx_list, total=len(txs))


def insert_update_model_action_tx(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> ModelActionTxType:
    repo = ModelActionTxRepo()
    if "transaction_uuid" not in kwargs:
        kwargs["transaction_uuid"] = etcd_client.new_id()
    key = repo.key(kwargs["model_action_uuid"], kwargs["transaction_uuid"])

    value = dict(
        model_action_uuid=kwargs["model_action_uuid"],
        transaction_uuid=kwargs["transaction_uuid"],
        endpoint_id=info.context["endpoint_id"],
        associated_model_uuid=kwargs["associated_model_uuid"],
        primary_key=kwargs.get("primary_key")
        or {"attribute": "order_id", "value": etcd_client.new_id(), "type": "string"},
        arguments=kwargs.get("arguments") or {},
        status=kwargs.get("status", "PENDING"),
        notes=kwargs.get("notes", ""),
        updated_by="system",
    )
    tx_data = repo.upsert(key, value)
    return ModelActionTxType(**repo._process_datetime_fields(tx_data))


def delete_model_action_tx(info: ResolveInfo, **kwargs: Dict[str, Any]) -> bool:
    repo = ModelActionTxRepo()
    model_action_uuid = kwargs["model_action_uuid"]
    transaction_uuid = kwargs["transaction_uuid"]

    success, blockers = repo.delete_safe(model_action_uuid, transaction_uuid)
    return success
