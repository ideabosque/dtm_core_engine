# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import List, Optional, Tuple

from ..handlers.etcd_client import delete_key as delkey
from ..handlers.etcd_client import iter_keys
from .base import BaseRepo
from .utils import ETCD_PREFIX


def k_pkmeta(associated_model_uuid, pkmeta_uuid):
    return f"{ETCD_PREFIX}/primary_key_metadata/{associated_model_uuid}/{pkmeta_uuid}"


def k_idx_associated_pkmeta(associated_model_uuid, pkmeta_uuid):
    return f"{ETCD_PREFIX}/index/by-associated/{associated_model_uuid}/pkmeta/{pkmeta_uuid}"


class PrimaryKeyMetaRepo(BaseRepo):
    def key(self, associated_model_uuid: str, pkmeta_uuid: str) -> str:
        return k_pkmeta(associated_model_uuid, pkmeta_uuid)

    def create(self, associated_model_uuid: str, pkmeta_uuid: str, **fields) -> bool:
        from ..handlers.etcd_client import now_iso

        value = dict(
            associated_model_uuid=associated_model_uuid,
            primary_key_metadata_uuid=pkmeta_uuid,
            attribute_name=fields.get("attribute_name", "order_id"),
            data_type=fields.get("data_type", "string"),
            key_type=fields.get("key_type", "HASH"),
            endpoint_id=fields.get("endpoint_id", "ep-1"),
            created_at=now_iso(),
            updated_at=now_iso(),
            updated_by="system",
        )
        idx = [k_idx_associated_pkmeta(associated_model_uuid, pkmeta_uuid)]
        return self.create_if_absent(
            self.key(associated_model_uuid, pkmeta_uuid), value, idx
        )

    def list(
        self,
        *,
        associated_model_uuid: Optional[str] = None,
        attribute_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        docs: List[dict] = []
        if associated_model_uuid:
            pk_ids = [
                k.rsplit("/", 1)[-1]
                for k in iter_keys(
                    f"{ETCD_PREFIX}/index/by-associated/{associated_model_uuid}/pkmeta/",
                    etcd=self.etcd,
                )
            ]
            for pk_id in pk_ids:
                doc = self.get(self.key(associated_model_uuid, pk_id))
                if doc:
                    docs.append(doc)
        else:
            for _k, payload in self._iter_prefix(
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
        delkey(
            k_idx_associated_pkmeta(associated_model_uuid, pkmeta_uuid), etcd=self.etcd
        )
        return True, []
