# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import List, Optional

import pendulum

from ..handlers import etcd_client


class BaseRepo:
    """
    Shared CRUD helpers. Note: these are single-writer safe.
    For multi-writer atomicity, upgrade to etcd Txn-based CAS.
    """

    def get(self, key: str) -> Optional[dict]:
        return etcd_client.get_json(key)

    def upsert(
        self, key: str, value: dict, index_keys: Optional[List[str]] = None
    ) -> dict:
        existing = etcd_client.get_json(key)
        now = etcd_client.now_iso()

        # Preserve created_at from existing record, set updated_at to now
        value["created_at"] = existing.get("created_at", now) if existing else now
        value["updated_at"] = now

        etcd_client.put_json(key, value)
        if index_keys:
            etcd_client.ensure_marker_keys(index_keys)
        return value

    def delete_key_only(self, key: str) -> bool:
        return etcd_client.delete_key(key)

    def _iter_prefix(self, prefix: str):
        return etcd_client.iter_prefix(prefix)

    def _process_datetime_fields(self, data: dict) -> dict:
        """Process datetime fields for GraphQL type creation"""
        result = data.copy()
        if "created_at" in result:
            result["created_at"] = pendulum.parse(result["created_at"])
        if "updated_at" in result:
            result["updated_at"] = pendulum.parse(result["updated_at"])
        return result
