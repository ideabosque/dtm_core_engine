# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import List, Optional, Tuple

from ..handlers.etcd_client import has_any, iter_prefix, new_id, now_iso
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_tx(model_action_uuid, transaction_uuid):
    return f"{ETCD_PREFIX}/model_action_tx/{model_action_uuid}/{transaction_uuid}"


class ModelActionTxRepo(BaseRepo):
    def key(self, model_action_uuid: str, transaction_uuid: str) -> str:
        return k_tx(model_action_uuid, transaction_uuid)

    def create(
        self,
        model_action_uuid: str,
        transaction_uuid: str,
        *,
        endpoint_id: str,
        associated_model_uuid: str,
        primary_key: dict | None = None,
        arguments: dict | None = None,
        status: str = "PENDING",
        notes: str = "",
    ) -> bool:
        value = dict(
            model_action_uuid=model_action_uuid,
            transaction_uuid=transaction_uuid,
            endpoint_id=endpoint_id,
            associated_model_uuid=associated_model_uuid,
            primary_key=primary_key
            or {"attribute": "order_id", "value": new_id(), "type": "string"},
            arguments=arguments or {},
            status=status,
            notes=notes,
            created_at=now_iso(),
            updated_at=now_iso(),
            updated_by="system",
        )
        return self.create_if_absent(
            self.key(model_action_uuid, transaction_uuid), value
        )

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
        if has_any(
            f"{ETCD_PREFIX}/associated_model_actions/{transaction_uuid}/",
            etcd=self.etcd,
        ):
            blockers.append("Associated model actions exist under this transaction")
        if blockers:
            return False, blockers
        ok = self.delete_key_only(self.key(model_action_uuid, transaction_uuid))
        return ok, ([] if ok else ["Delete failed"])
