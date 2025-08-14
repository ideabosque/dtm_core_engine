# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import List, Optional, Tuple

from ..handlers.etcd_client import delete_key as delkey
from ..handlers.etcd_client import has_any, iter_keys, now_iso
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_model_actions(endpoint_id, model_action_uuid):
    return f"{ETCD_PREFIX}/model_actions/{endpoint_id}/{model_action_uuid}"


def k_idx_endpoint_actions(endpoint_id, model_action_uuid):
    return f"{ETCD_PREFIX}/index/by-endpoint/{endpoint_id}/model_actions/{model_action_uuid}"


class ModelActionRepo(BaseRepo):
    def key(self, endpoint_id: str, model_action_uuid: str) -> str:
        return k_model_actions(endpoint_id, model_action_uuid)

    def create(
        self,
        endpoint_id: str,
        model_action_uuid: str,
        *,
        model_uuid: str,
        action_name: str,
        associated_model_uuids: List[str],
    ) -> bool:
        value = dict(
            model_action_uuid=model_action_uuid,
            endpoint_id=endpoint_id,
            model_uuid=model_uuid,
            action_name=action_name,
            associated_model_uuids=associated_model_uuids,
            created_at=now_iso(),
            updated_at=now_iso(),
            updated_by="system",
        )
        idx = [k_idx_endpoint_actions(endpoint_id, model_action_uuid)]
        return self.create_if_absent(
            self.key(endpoint_id, model_action_uuid), value, idx
        )

    def list(
        self,
        *,
        endpoint_id: Optional[str] = None,
        model_uuid: Optional[str] = None,
        action_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        docs: List[dict] = []
        if endpoint_id:
            ids = [
                k.rsplit("/", 1)[-1]
                for k in iter_keys(
                    f"{ETCD_PREFIX}/index/by-endpoint/{endpoint_id}/model_actions/",
                    etcd=self.etcd,
                )
            ]
            for mid in ids:
                doc = self.get(self.key(endpoint_id, mid))
                if doc:
                    docs.append(doc)
        else:
            for _k, payload in self._iter_prefix(f"{ETCD_PREFIX}/model_actions/"):
                if payload:
                    docs.append(payload)

        if model_uuid:
            docs = [d for d in docs if match(d, model_uuid=model_uuid)]
        if action_name:
            docs = [d for d in docs if match(d, action_name=action_name)]
        if limit:
            docs = docs[:limit]
        return docs

    def delete_safe(
        self, endpoint_id: str, model_action_uuid: str
    ) -> Tuple[bool, List[str]]:
        blockers: List[str] = []
        if has_any(
            f"{ETCD_PREFIX}/model_action_tx/{model_action_uuid}/", etcd=self.etcd
        ):
            blockers.append("Transactions exist for this model action")
        if blockers:
            return False, blockers
        ok = self.delete_key_only(self.key(endpoint_id, model_action_uuid))
        if not ok:
            return False, ["Delete failed"]
        delkey(k_idx_endpoint_actions(endpoint_id, model_action_uuid), etcd=self.etcd)
        return True, []
