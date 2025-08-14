# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import List, Optional, Tuple

from ..handlers.etcd_client import iter_keys
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_associated_models(endpoint_id, associated_model_uuid):
    return f"{ETCD_PREFIX}/associated_models/{endpoint_id}/{associated_model_uuid}"


def k_idx_model_associated(model_uuid, associated_model_uuid):
    return (
        f"{ETCD_PREFIX}/index/by-model/{model_uuid}/associated/{associated_model_uuid}"
    )


class AssociatedModelRepo(BaseRepo):
    def key(self, endpoint_id: str, associated_model_uuid: str) -> str:
        return k_associated_models(endpoint_id, associated_model_uuid)

    def create(
        self,
        endpoint_id: str,
        associated_model_uuid: str,
        *,
        model_uuid: str,
        actions: dict,
    ) -> bool:
        from ..handlers.etcd_client import now_iso

        value = dict(
            associated_model_uuid=associated_model_uuid,
            endpoint_id=endpoint_id,
            model_uuid=model_uuid,
            actions=actions,
            created_at=now_iso(),
            updated_at=now_iso(),
            updated_by="system",
        )
        idx = [k_idx_model_associated(model_uuid, associated_model_uuid)]
        return self.create_if_absent(
            self.key(endpoint_id, associated_model_uuid), value, idx
        )

    def list(
        self,
        *,
        endpoint_id: Optional[str] = None,
        model_uuid: Optional[str] = None,
        action_name_contains: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        docs: List[dict] = []
        if model_uuid:
            assoc_ids = [
                k.rsplit("/", 1)[-1]
                for k in iter_keys(
                    f"{ETCD_PREFIX}/index/by-model/{model_uuid}/associated/",
                    etcd=self.etcd,
                )
            ]
            if endpoint_id:
                for assoc_id in assoc_ids:
                    doc = self.get(self.key(endpoint_id, assoc_id))
                    if doc:
                        docs.append(doc)
            else:
                need = set(assoc_ids)
                for _k, payload in self._iter_prefix(
                    f"{ETCD_PREFIX}/associated_models/"
                ):
                    if payload and payload.get("associated_model_uuid") in need:
                        docs.append(payload)
                        need.discard(payload["associated_model_uuid"])
                        if not need:
                            break
        else:
            prefix = (
                f"{ETCD_PREFIX}/associated_models/{endpoint_id}/"
                if endpoint_id
                else f"{ETCD_PREFIX}/associated_models/"
            )
            for _k, payload in self._iter_prefix(prefix):
                if payload:
                    docs.append(payload)

        if action_name_contains:
            docs = [
                d
                for d in docs
                if any(
                    action_name_contains in name
                    for name in (d.get("actions") or {}).keys()
                )
            ]
        if limit:
            docs = docs[:limit]
        return docs

    def delete_safe(
        self, endpoint_id: str, associated_model_uuid: str, *, model_uuid: str
    ) -> Tuple[bool, List[str]]:
        from ..handlers.etcd_client import delete_key as delkey
        from ..handlers.etcd_client import has_any
        from ..handlers.etcd_client import iter_prefix as _iter

        blockers: List[str] = []

        if has_any(
            f"{ETCD_PREFIX}/index/by-associated/{associated_model_uuid}/pkmeta/",
            etcd=self.etcd,
        ) or has_any(
            f"{ETCD_PREFIX}/primary_key_metadata/{associated_model_uuid}/",
            etcd=self.etcd,
        ):
            blockers.append("PrimaryKey metadata exist for this associated model")
        for _k, doc in _iter(f"{ETCD_PREFIX}/model_action_tx/", etcd=self.etcd):
            if doc and doc.get("associated_model_uuid") == associated_model_uuid:
                blockers.append(
                    f"Transactions exist (e.g., tx {doc.get('transaction_uuid')})"
                )
                break
        for _k, doc in _iter(f"{ETCD_PREFIX}/model_actions/", etcd=self.etcd):
            if doc and associated_model_uuid in (
                doc.get("associated_model_uuids") or []
            ):
                blockers.append(
                    f"ModelAction {doc.get('model_action_uuid')} references this associated model"
                )
                break

        if blockers:
            return False, blockers

        ok = self.delete_key_only(self.key(endpoint_id, associated_model_uuid))
        if not ok:
            return False, ["Delete failed"]

        delkey(
            k_idx_model_associated(model_uuid, associated_model_uuid), etcd=self.etcd
        )
        return True, []
