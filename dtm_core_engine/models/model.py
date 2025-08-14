# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import List, Optional, Tuple

from ..handlers.etcd_client import now_iso
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_models(module_uuid, model_uuid):
    return f"{ETCD_PREFIX}/models/{module_uuid}/{model_uuid}"


class ModelRepo(BaseRepo):
    def key(self, module_uuid: str, model_uuid: str) -> str:
        return k_models(module_uuid, model_uuid)

    def create(self, module_uuid: str, model_uuid: str, **fields) -> bool:
        value = dict(
            model_uuid=model_uuid,
            module_uuid=module_uuid,
            model_name=fields.get("model_name", "Order"),
            endpoint_id=fields.get("endpoint_id", "ep-1"),
            created_at=now_iso(),
            updated_at=now_iso(),
            updated_by="system",
        )
        return self.create_if_absent(self.key(module_uuid, model_uuid), value)

    def list(
        self,
        *,
        module_uuid: Optional[str] = None,
        model_name: Optional[str] = None,
        endpoint_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        prefix = (
            f"{ETCD_PREFIX}/models/{module_uuid}/"
            if module_uuid
            else f"{ETCD_PREFIX}/models/"
        )
        results: List[dict] = []
        for _k, payload in self._iter_prefix(prefix):
            if not payload:
                continue
            if model_name and not match(payload, model_name__contains=model_name):
                continue
            if endpoint_id and not match(payload, endpoint_id=endpoint_id):
                continue
            results.append(payload)
            if limit and len(results) >= limit:
                break
        return results

    def delete_safe(self, module_uuid: str, model_uuid: str) -> Tuple[bool, List[str]]:
        from ..handlers.etcd_client import has_any
        from ..handlers.etcd_client import iter_prefix as _iter

        blockers: List[str] = []
        if has_any(
            f"{ETCD_PREFIX}/index/by-model/{model_uuid}/associated/", etcd=self.etcd
        ):
            blockers.append("Associated models exist for this model")
        for _k, doc in _iter(f"{ETCD_PREFIX}/model_actions/", etcd=self.etcd):
            if doc and doc.get("model_uuid") == model_uuid:
                blockers.append(
                    f"ModelAction {doc.get('model_action_uuid')} references this model"
                )
                break
        if blockers:
            return False, blockers
        ok = self.delete_key_only(self.key(module_uuid, model_uuid))
        return ok, ([] if ok else ["Delete failed"])
