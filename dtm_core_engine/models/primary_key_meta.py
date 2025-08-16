# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict, List, Optional, Tuple

from graphene import ResolveInfo

from ..handlers import etcd_client
from ..types.primary_key_meta import PrimaryKeyMetaListType, PrimaryKeyMetaType
from .base import BaseRepo
from .utils import ETCD_PREFIX


def k_pkmeta(associated_model_uuid, pkmeta_uuid):
    return f"{ETCD_PREFIX}/primary_key_metadata/{associated_model_uuid}/{pkmeta_uuid}"


def k_idx_associated_pkmeta(associated_model_uuid, pkmeta_uuid):
    return f"{ETCD_PREFIX}/index/by-associated/{associated_model_uuid}/pkmeta/{pkmeta_uuid}"


class PrimaryKeyMetaRepo(BaseRepo):
    def key(self, associated_model_uuid: str, pkmeta_uuid: str) -> str:
        return k_pkmeta(associated_model_uuid, pkmeta_uuid)

    def list(
        self,
        *,
        associated_model_uuid: Optional[str] = None,
        attribute_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        docs: List[dict] = []
        if associated_model_uuid:
            # Try index-based lookup first
            pk_ids = [
                k.rsplit("/", 1)[-1]
                for k in etcd_client.iter_keys(
                    f"{ETCD_PREFIX}/index/by-associated/{associated_model_uuid}/pkmeta/"
                )
            ]
            for pk_id in pk_ids:
                doc = etcd_client.get_json(self.key(associated_model_uuid, pk_id))
                if doc:
                    docs.append(doc)

            # Fallback to direct prefix scan if index is empty
            if not docs:
                for _k, payload in etcd_client.iter_prefix(
                    f"{ETCD_PREFIX}/primary_key_metadata/{associated_model_uuid}/"
                ):
                    if payload:
                        docs.append(payload)
        else:
            for _k, payload in etcd_client.iter_prefix(
                f"{ETCD_PREFIX}/primary_key_metadata/"
            ):
                if payload:
                    docs.append(payload)
        if attribute_name:
            docs = [d for d in docs if d.get("attribute_name") == attribute_name]
        if limit:
            docs = docs[:limit]
        return docs

    def delete_safe(
        self, associated_model_uuid: str, pkmeta_uuid: str
    ) -> Tuple[bool, List[str]]:
        ok = self.delete_key_only(self.key(associated_model_uuid, pkmeta_uuid))
        if not ok:
            return False, ["Delete failed"]
        etcd_client.delete_key(
            k_idx_associated_pkmeta(associated_model_uuid, pkmeta_uuid)
        )
        return True, []


def resolve_primary_key_meta(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> PrimaryKeyMetaType:
    repo = PrimaryKeyMetaRepo()
    primary_key_metadata_uuid = kwargs.get("primary_key_metadata_uuid")
    associated_model_uuid = kwargs.get("associated_model_uuid")

    if primary_key_metadata_uuid and associated_model_uuid:
        # Direct lookup by UUID
        key = repo.key(associated_model_uuid, primary_key_metadata_uuid)
        meta_data = repo.get(key)
        if not meta_data:
            return None
    else:
        # List lookup
        metas = repo.list(
            associated_model_uuid=associated_model_uuid,
            attribute_name=kwargs.get("attribute_name"),
            limit=1,
        )
        if not metas:
            return None
        meta_data = metas[0]

    return PrimaryKeyMetaType(**repo._process_datetime_fields(meta_data))


def resolve_primary_key_meta_list(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> PrimaryKeyMetaListType:
    repo = PrimaryKeyMetaRepo()
    metas = repo.list(
        associated_model_uuid=kwargs.get("associated_model_uuid"),
        attribute_name=kwargs.get("attribute_name"),
        limit=kwargs.get("limit"),
    )
    meta_list = [PrimaryKeyMetaType(**repo._process_datetime_fields(m)) for m in metas]
    return PrimaryKeyMetaListType(primary_key_meta_list=meta_list, total=len(metas))


def insert_update_primary_key_meta(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> PrimaryKeyMetaType:
    repo = PrimaryKeyMetaRepo()
    if "primary_key_metadata_uuid" not in kwargs:
        kwargs["primary_key_metadata_uuid"] = f"pk-{etcd_client.new_id()[:8]}"
    key = repo.key(kwargs["associated_model_uuid"], kwargs["primary_key_metadata_uuid"])

    value = dict(
        associated_model_uuid=kwargs["associated_model_uuid"],
        primary_key_metadata_uuid=kwargs["primary_key_metadata_uuid"],
        attribute_name=kwargs.get("attribute_name", "order_id"),
        data_type=kwargs.get("data_type", "string"),
        key_type=kwargs.get("key_type", "HASH"),
        endpoint_id=info.context["endpoint_id"],
        updated_by="system",
    )
    idx_key = k_idx_associated_pkmeta(
        kwargs["associated_model_uuid"], kwargs["primary_key_metadata_uuid"]
    )
    meta_data = repo.upsert(key, value, [idx_key])
    return PrimaryKeyMetaType(**repo._process_datetime_fields(meta_data))


def delete_primary_key_meta(info: ResolveInfo, **kwargs: Dict[str, Any]) -> bool:
    repo = PrimaryKeyMetaRepo()
    associated_model_uuid = kwargs["associated_model_uuid"]
    pkmeta_uuid = kwargs["primary_key_metadata_uuid"]

    success, blockers = repo.delete_safe(associated_model_uuid, pkmeta_uuid)
    return success
