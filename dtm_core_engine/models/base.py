# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Callable, Dict, List, Optional

from ..handlers.etcd_client import (
    delete_key,
    ensure_marker_keys,
    get_client,
    get_json,
    iter_keys,
    iter_prefix,
    now_iso,
    put_json,
)


class BaseRepo:
    """
    Shared CRUD helpers. Note: these are single-writer safe.
    For multi-writer atomicity, upgrade to etcd Txn-based CAS.
    """

    def __init__(self, *, etcd=None):
        self.etcd = etcd or get_client()

    def create_if_absent(
        self, key: str, value: dict, index_keys: Optional[List[str]] = None
    ) -> bool:
        if get_json(key, etcd=self.etcd) is not None:
            return False
        put_json(key, value, etcd=self.etcd)
        if index_keys:
            ensure_marker_keys(index_keys, etcd=self.etcd)
        return True

    def get(self, key: str) -> Optional[dict]:
        return get_json(key, etcd=self.etcd)

    def update(self, key: str, patch: Dict[str, Any]) -> bool:
        doc = get_json(key, etcd=self.etcd)
        if doc is None:
            return False
        doc.update(patch)
        doc["updated_at"] = now_iso()
        put_json(key, doc, etcd=self.etcd)
        return True

    def delete_key_only(self, key: str) -> bool:
        return delete_key(key, etcd=self.etcd)

    # generic list helper over a prefix
    def _list_from_prefix(
        self,
        prefix: str,
        *,
        where: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        key_to_id: Optional[Callable[[str], str]] = None,
    ) -> List[dict]:
        results: List[dict] = []
        for key, payload in iter_prefix(prefix, etcd=self.etcd):
            if not payload:
                continue
            if where:
                matched = True
                for k, v in where.items():
                    if "__" not in k and payload.get(k) != v:
                        matched = False
                        break
                if not matched:
                    continue
            results.append(payload if key_to_id is None else payload)
            if limit and len(results) >= limit:
                break
        return results

    def _iter_prefix(self, prefix: str):
        return iter_prefix(prefix, etcd=self.etcd)

    def _iter_keys(self, prefix: str):
        return iter_keys(prefix, etcd=self.etcd)
