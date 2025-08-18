# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict, List, Optional, Tuple

from graphene import ResolveInfo

from ..handlers import etcd_client
from ..types.data_source import DataSourceListType, DataSourceType
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_data_sources(endpoint_id, data_source_uuid):
    return f"{ETCD_PREFIX}/data_sources/{endpoint_id}/{data_source_uuid}"


class DataSourceRepo(BaseRepo):
    def key(self, endpoint_id: str, data_source_uuid: str) -> str:
        return k_data_sources(endpoint_id, data_source_uuid)

    def list(
        self,
        *,
        endpoint_id: Optional[str] = None,
        data_source_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        prefix = (
            f"{ETCD_PREFIX}/data_sources/{endpoint_id}/"
            if endpoint_id
            else f"{ETCD_PREFIX}/data_sources/"
        )
        results: List[dict] = []
        for _k, payload in self._iter_prefix(prefix):
            if not payload:
                continue
            if data_source_name and not match(
                payload, data_source_name__contains=data_source_name
            ):
                continue
            results.append(payload)
            if limit and len(results) >= limit:
                break
        return results

    def delete_safe(
        self, endpoint_id: str, data_source_uuid: str
    ) -> Tuple[bool, List[str]]:
        blockers: List[str] = []
        if etcd_client.has_any(f"{ETCD_PREFIX}/modules/{endpoint_id}/"):
            for _k, doc in etcd_client.iter_prefix(
                f"{ETCD_PREFIX}/modules/{endpoint_id}/"
            ):
                if doc and doc.get("data_source_uuid") == data_source_uuid:
                    blockers.append("Modules exist using this data source")
                    break
        if blockers:
            return False, blockers
        ok = self.delete_key_only(self.key(endpoint_id, data_source_uuid))
        return ok, ([] if ok else ["Delete failed"])


def resolve_data_source(info: ResolveInfo, **kwargs: Dict[str, Any]) -> DataSourceType:
    repo = DataSourceRepo()
    data_source_uuid = kwargs.get("data_source_uuid")
    if data_source_uuid:
        key = repo.key(info.context["endpoint_id"], data_source_uuid)
        data_source_data = repo.get(key)
        if not data_source_data:
            return None
        return DataSourceType(**repo._process_datetime_fields(data_source_data))
    else:
        data_sources = repo.list(
            endpoint_id=info.context["endpoint_id"],
            data_source_name=kwargs.get("data_source_name"),
            limit=1,
        )
        if not data_sources:
            return None
        return DataSourceType(**repo._process_datetime_fields(data_sources[0]))


def resolve_data_source_list(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> DataSourceListType:
    repo = DataSourceRepo()
    data_sources = repo.list(
        endpoint_id=info.context["endpoint_id"],
        data_source_name=kwargs.get("data_source_name"),
        limit=kwargs.get("limit"),
    )
    data_source_list = [
        DataSourceType(**repo._process_datetime_fields(ds)) for ds in data_sources
    ]
    return DataSourceListType(
        data_source_list=data_source_list, total=len(data_sources)
    )


def insert_update_data_source(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> DataSourceType:
    repo = DataSourceRepo()
    endpoint_id = info.context["endpoint_id"]
    if "data_source_uuid" not in kwargs:
        kwargs["data_source_uuid"] = f"dts-{etcd_client.new_id()[:8]}"
    key = repo.key(endpoint_id, kwargs["data_source_uuid"])

    value = dict(
        data_source_uuid=kwargs["data_source_uuid"],
        endpoint_id=endpoint_id,
        data_source_name=kwargs.get("data_source_name", "demo-data-source"),
        setting=kwargs.get("setting", {}),
        connector_class_name=kwargs.get("connector_class_name"),
        connector_module_name=kwargs.get("connector_module_name"),
        connector_package_name=kwargs.get("connector_package_name"),
        updated_by=kwargs.get("updated_by", "system"),
    )
    data_source_data = repo.upsert(key, value)
    return DataSourceType(**repo._process_datetime_fields(data_source_data))


def delete_data_source(info: ResolveInfo, **kwargs: Dict[str, Any]) -> bool:
    repo = DataSourceRepo()
    endpoint_id = info.context["endpoint_id"]
    data_source_uuid = kwargs["data_source_uuid"]

    success, blockers = repo.delete_safe(endpoint_id, data_source_uuid)
    return success
