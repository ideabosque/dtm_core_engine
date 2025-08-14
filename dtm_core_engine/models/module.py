# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import List, Optional, Tuple

from ..handlers.etcd_client import new_id, now_iso
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_modules(endpoint_id, module_uuid):
    return f"{ETCD_PREFIX}/modules/{endpoint_id}/{module_uuid}"


class ModuleRepo(BaseRepo):
    def key(self, endpoint_id: str, module_uuid: str) -> str:
        return k_modules(endpoint_id, module_uuid)

    def create(self, endpoint_id: str, module_uuid: str, **fields) -> bool:
        value = dict(
            module_uuid=module_uuid,
            endpoint_id=endpoint_id,
            module_name=fields.get("module_name", "demo-module"),
            package_name=fields.get("package_name", "demo.pkg"),
            data_source_uuid=fields.get("data_source_uuid", new_id()),
            source=fields.get("source", "internal"),
            created_at=now_iso(),
            updated_at=now_iso(),
            updated_by=fields.get("updated_by", "system"),
        )
        return self.create_if_absent(self.key(endpoint_id, module_uuid), value)

    def list(
        self,
        *,
        endpoint_id: Optional[str] = None,
        module_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        prefix = (
            f"{ETCD_PREFIX}/modules/{endpoint_id}/"
            if endpoint_id
            else f"{ETCD_PREFIX}/modules/"
        )
        results: List[dict] = []
        for _k, payload in self._iter_prefix(prefix):
            if not payload:
                continue
            if module_name and not match(payload, module_name__contains=module_name):
                continue
            results.append(payload)
            if limit and len(results) >= limit:
                break
        return results

    def delete_safe(self, endpoint_id: str, module_uuid: str) -> Tuple[bool, List[str]]:
        from ..handlers.etcd_client import has_any

        blockers: List[str] = []
        if has_any(f"{ETCD_PREFIX}/models/{module_uuid}/", etcd=self.etcd):
            blockers.append("Models exist under this module")
        if blockers:
            return False, blockers
        ok = self.delete_key_only(self.key(endpoint_id, module_uuid))
        return ok, ([] if ok else ["Delete failed"])
