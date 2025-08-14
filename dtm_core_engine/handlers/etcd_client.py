# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import json
import time
import uuid
from typing import Any, Iterable, List, Optional, Tuple

from etcd3gw import client as etcd3

_ETCD: Optional[object] = None


def get_client(host: str = "127.0.0.1", port: int = 2379):
    """Return a process-wide etcd3gw client (lazy singleton)."""
    global _ETCD
    if _ETCD is None:
        _ETCD = etcd3(host=host, port=port)
    return _ETCD


# ---------- time/id helpers ----------


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def new_id() -> str:
    return uuid.uuid4().hex


# ---------- JSON & client helpers ----------


def jdump(obj: dict) -> bytes:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode()


def _to_json(value: Any):
    if value is None:
        return None
    if isinstance(value, (bytes, bytearray)):
        if not value:
            return None
        return json.loads(value.decode())
    if isinstance(value, str):
        if value == "":
            return None
        return json.loads(value)
    return value


def get_json(key: str, *, etcd=None):
    cli = etcd or get_client()
    res = cli.get(key)
    if not res:
        return None
    if isinstance(res, list):
        if len(res) == 0:
            return None
        first = res[0]
        if isinstance(first, tuple):
            return _to_json(first[0])
        if isinstance(first, dict) and "value" in first:
            return _to_json(first["value"])
        return _to_json(first)
    return _to_json(res)


def put_json(key: str, value: dict, *, etcd=None) -> None:
    cli = etcd or get_client()
    cli.put(key, jdump(value))


# ---------- scans ----------


def iter_prefix(prefix: str, *, etcd=None) -> Iterable[Tuple[str, Optional[dict]]]:
    """Yield (key, payload_or_None). Empty values (index markers) return None."""
    cli = etcd or get_client()
    for val, meta in cli.get_prefix(prefix):
        key = meta.get("key")
        if isinstance(key, (bytes, bytearray)):
            key = key.decode()
        if isinstance(val, (bytes, bytearray)) and len(val) > 0:
            yield key, json.loads(val.decode())
        elif isinstance(val, str) and val != "":
            yield key, json.loads(val)
        else:
            yield key, None


def iter_keys(prefix: str, *, etcd=None) -> Iterable[str]:
    cli = etcd or get_client()
    for _val, meta in cli.get_prefix(prefix):
        key = meta.get("key")
        yield key.decode() if isinstance(key, (bytes, bytearray)) else key


# ---------- index/cleanup helpers ----------


def ensure_marker_keys(index_keys: List[str], *, etcd=None) -> None:
    cli = etcd or get_client()
    for ikey in index_keys:
        cli.put(ikey, b"")


def delete_key(key: str, *, etcd=None) -> bool:
    cli = etcd or get_client()
    return cli.delete(key) is True


def delete_prefix(prefix: str, *, etcd=None) -> None:
    cli = etcd or get_client()
    cli.delete_prefix(prefix)


def has_any(prefix: str, *, etcd=None) -> bool:
    for _ in iter_keys(prefix, etcd=etcd):
        return True
    return False
