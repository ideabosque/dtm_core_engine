# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import json
import uuid
from typing import Iterable, List, Optional, Tuple

import pendulum
from etcd3gw import client as etcd3

_ETCD = None


def get_client():
    global _ETCD
    if _ETCD is None:
        from .config import Config

        _ETCD = etcd3(host=Config.etcd_host, port=Config.etcd_port)
    return _ETCD


def now_iso() -> str:
    return pendulum.now("UTC").to_iso8601_string()


def new_id() -> str:
    return uuid.uuid4().hex


def get_json(key: str):
    res = get_client().get(key)
    if not res or (isinstance(res, list) and len(res) == 0):
        return None

    # Handle etcd3gw response format: [(value, metadata), ...]
    if isinstance(res, list) and len(res) > 0:
        val = res[0][0] if isinstance(res[0], tuple) else res[0]
    else:
        val = res

    if isinstance(val, (bytes, bytearray)) and val:
        return json.loads(val.decode())
    elif isinstance(val, str) and val:
        return json.loads(val)
    return None


def put_json(key: str, value: dict) -> None:
    data = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    get_client().put(key, data)


def iter_prefix(prefix: str) -> Iterable[Tuple[str, Optional[dict]]]:
    for val, meta in get_client().get_prefix(prefix):
        key = meta.get("key")
        if isinstance(key, (bytes, bytearray)):
            key = key.decode()
        if isinstance(val, (bytes, bytearray)) and len(val) > 0:
            yield key, json.loads(val.decode())
        elif isinstance(val, str) and val:
            yield key, json.loads(val)
        else:
            yield key, None


def iter_keys(prefix: str) -> Iterable[str]:
    for _val, meta in get_client().get_prefix(prefix):
        key = meta.get("key")
        yield key.decode() if isinstance(key, (bytes, bytearray)) else key


def ensure_marker_keys(index_keys: List[str]) -> None:
    cli = get_client()
    for ikey in index_keys:
        cli.put(ikey, b"")


def delete_key(key: str) -> bool:
    return get_client().delete(key) is True


def has_any(prefix: str) -> bool:
    for _ in iter_keys(prefix):
        return True
    return False
