# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict, List, Optional, Tuple

import pendulum
from graphene import ResolveInfo

from silvaengine_utility import Utility

from ..handlers import etcd_client
from ..types.module import ModuleListType, ModuleType
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_modules(endpoint_id, module_uuid):
    return f"{ETCD_PREFIX}/modules/{endpoint_id}/{module_uuid}"


class ModuleRepo(BaseRepo):
    def key(self, endpoint_id: str, module_uuid: str) -> str:
        return k_modules(endpoint_id, module_uuid)

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
        blockers: List[str] = []
        if etcd_client.has_any(f"{ETCD_PREFIX}/models/{module_uuid}/"):
            blockers.append("Models exist under this module")
        if blockers:
            return False, blockers
        ok = self.delete_key_only(self.key(endpoint_id, module_uuid))
        return ok, ([] if ok else ["Delete failed"])


def resolve_module(info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModuleType:
    repo = ModuleRepo()
    module_uuid = kwargs.get("module_uuid")
    if module_uuid:
        # Direct lookup by UUID
        key = repo.key(info.context["endpoint_id"], module_uuid)
        module_data = repo.get(key)
        if not module_data:
            return None
        return ModuleType(**repo._process_datetime_fields(module_data))
    else:
        # List lookup by module_name
        modules = repo.list(
            endpoint_id=info.context["endpoint_id"],
            module_name=kwargs.get("module_name"),
            limit=1,
        )
        if not modules:
            return None
        return ModuleType(**repo._process_datetime_fields(modules[0]))


def resolve_module_list(info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModuleListType:
    repo = ModuleRepo()
    modules = repo.list(
        endpoint_id=info.context["endpoint_id"],
        module_name=kwargs.get("module_name"),
        limit=kwargs.get("limit"),
    )
    module_list = [ModuleType(**repo._process_datetime_fields(m)) for m in modules]
    return ModuleListType(module_list=module_list, total=len(modules))


def insert_update_module(info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModuleType:
    repo = ModuleRepo()
    endpoint_id = info.context["endpoint_id"]
    if "module_uuid" not in kwargs:
        kwargs["module_uuid"] = f"mod-{etcd_client.new_id()[:8]}"
    key = repo.key(endpoint_id, kwargs["module_uuid"])

    # Handle data_source_uuid special case - preserve existing or generate new
    existing = repo.get(key)
    data_source_uuid = kwargs.get("data_source_uuid") or (
        existing.get("data_source_uuid") if existing else etcd_client.new_id()
    )

    value = dict(
        module_uuid=kwargs["module_uuid"],
        endpoint_id=endpoint_id,
        module_name=kwargs.get("module_name", "demo-module"),
        package_name=kwargs.get("package_name", "demo.pkg"),
        data_source_uuid=data_source_uuid,
        source=kwargs.get("source", "internal"),
        updated_by=kwargs.get("updated_by", "system"),
    )
    module_data = repo.upsert(key, value)
    return ModuleType(**repo._process_datetime_fields(module_data))


def delete_module(info: ResolveInfo, **kwargs: Dict[str, Any]) -> bool:
    repo = ModuleRepo()
    endpoint_id = info.context["endpoint_id"]
    module_uuid = kwargs["module_uuid"]

    success, blockers = repo.delete_safe(endpoint_id, module_uuid)
    return success
