# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import List, Optional, Tuple

from ..handlers.etcd_client import now_iso
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_associated_actions(transaction_uuid, action_name):
    return f"{ETCD_PREFIX}/associated_model_actions/{transaction_uuid}/{action_name}"


class AssociatedModelActionRepo(BaseRepo):
    def key(self, transaction_uuid: str, action_name: str) -> str:
        return k_associated_actions(transaction_uuid, action_name)

    def insert(
        self,
        transaction_uuid: str,
        action_name: str,
        *,
        model_action_uuid: str,
        status: str = "NEW",
        response: dict | None = None,
        notes: str = "",
    ) -> bool:
        value = dict(
            transaction_uuid=transaction_uuid,
            action_name=action_name,
            model_action_uuid=model_action_uuid,
            status=status,
            response=response or {},
            notes=notes,
            created_at=now_iso(),
            updated_at=now_iso(),
            updated_by="worker-1",
        )
        return self.create_if_absent(self.key(transaction_uuid, action_name), value)

    def list(
        self,
        *,
        transaction_uuid: Optional[str] = None,
        status: Optional[str] = None,
        action_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        docs: List[dict] = []
        if transaction_uuid:
            for _k, payload in self._iter_prefix(
                f"{ETCD_PREFIX}/associated_model_actions/{transaction_uuid}/"
            ):
                if payload:
                    docs.append(payload)
        else:
            for _k, payload in self._iter_prefix(
                f"{ETCD_PREFIX}/associated_model_actions/"
            ):
                if payload:
                    docs.append(payload)
        if status:
            docs = [d for d in docs if match(d, status=status)]
        if action_name:
            docs = [d for d in docs if match(d, action_name=action_name)]
        if limit:
            docs = docs[:limit]
        return docs

    def delete_safe(
        self, transaction_uuid: str, action_name: str
    ) -> Tuple[bool, List[str]]:
        ok = self.delete_key_only(self.key(transaction_uuid, action_name))
        return ok, ([] if ok else ["Delete failed"])
