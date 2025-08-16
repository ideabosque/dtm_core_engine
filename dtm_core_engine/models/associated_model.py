# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict, List, Optional, Tuple

from graphene import ResolveInfo

from ..handlers import etcd_client
from ..types.associated_model import AssociatedModelListType, AssociatedModelType
from .base import BaseRepo
from .utils import ETCD_PREFIX


def k_associated_models(endpoint_id, associated_model_uuid):
    return f"{ETCD_PREFIX}/associated_models/{endpoint_id}/{associated_model_uuid}"


def k_idx_model_associated(model_uuid, associated_model_uuid):
    return (
        f"{ETCD_PREFIX}/index/by-model/{model_uuid}/associated/{associated_model_uuid}"
    )


class AssociatedModelRepo(BaseRepo):
    def key(self, endpoint_id: str, associated_model_uuid: str) -> str:
        return k_associated_models(endpoint_id, associated_model_uuid)

    def list(
        self,
        *,
        endpoint_id: Optional[str] = None,
        model_uuid: Optional[str] = None,
        action_name_contains: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        docs: List[dict] = []
        if model_uuid:
            assoc_ids = [
                k.rsplit("/", 1)[-1]
                for k in etcd_client.iter_keys(
                    f"{ETCD_PREFIX}/index/by-model/{model_uuid}/associated/"
                )
            ]
            if endpoint_id:
                for assoc_id in assoc_ids:
                    doc = self.get(self.key(endpoint_id, assoc_id))
                    if doc:
                        docs.append(doc)
            else:
                need = set(assoc_ids)
                for _k, payload in self._iter_prefix(
                    f"{ETCD_PREFIX}/associated_models/"
                ):
                    if payload and payload.get("associated_model_uuid") in need:
                        docs.append(payload)
                        need.discard(payload["associated_model_uuid"])
                        if not need:
                            break
        else:
            prefix = (
                f"{ETCD_PREFIX}/associated_models/{endpoint_id}/"
                if endpoint_id
                else f"{ETCD_PREFIX}/associated_models/"
            )
            for _k, payload in self._iter_prefix(prefix):
                if payload:
                    docs.append(payload)

        if action_name_contains:
            docs = [
                d
                for d in docs
                if any(
                    action_name_contains in name
                    for name in (d.get("actions") or {}).keys()
                )
            ]
        if limit:
            docs = docs[:limit]
        return docs

    def delete_safe(
        self, endpoint_id: str, associated_model_uuid: str, *, model_uuid: str
    ) -> Tuple[bool, List[str]]:

        blockers: List[str] = []

        if etcd_client.has_any(
            f"{ETCD_PREFIX}/index/by-associated/{associated_model_uuid}/pkmeta/"
        ) or etcd_client.has_any(
            f"{ETCD_PREFIX}/primary_key_metadata/{associated_model_uuid}/"
        ):
            blockers.append("PrimaryKey metadata exist for this associated model")
        for _k, doc in etcd_client.iter_prefix(f"{ETCD_PREFIX}/model_action_tx/"):
            if doc and doc.get("associated_model_uuid") == associated_model_uuid:
                blockers.append(
                    f"Transactions exist (e.g., tx {doc.get('transaction_uuid')})"
                )
                break
        for _k, doc in etcd_client.iter_prefix(f"{ETCD_PREFIX}/model_actions/"):
            if doc and associated_model_uuid in (
                doc.get("associated_model_uuids") or []
            ):
                blockers.append(
                    f"ModelAction {doc.get('model_action_uuid')} references this associated model"
                )
                break

        if blockers:
            return False, blockers

        ok = self.delete_key_only(self.key(endpoint_id, associated_model_uuid))
        if not ok:
            return False, ["Delete failed"]

        etcd_client.delete_key(
            k_idx_model_associated(model_uuid, associated_model_uuid)
        )
        return True, []


def resolve_associated_model(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> AssociatedModelType:
    repo = AssociatedModelRepo()
    associated_model_uuid = kwargs.get("associated_model_uuid")
    if associated_model_uuid:
        # Direct lookup by UUID
        key = repo.key(info.context["endpoint_id"], associated_model_uuid)
        model_data = etcd_client.get_json(key)
        if not model_data:
            # Fallback to list search if direct lookup fails
            models = repo.list(endpoint_id=info.context["endpoint_id"], limit=None)
            for model in models:
                if model.get("associated_model_uuid") == associated_model_uuid:
                    model_data = model
                    break
            if not model_data:
                return None
    else:
        # List lookup
        models = repo.list(
            endpoint_id=info.context["endpoint_id"],
            model_uuid=kwargs.get("model_uuid"),
            action_name_contains=kwargs.get("action_name_contains"),
            limit=1,
        )
        if not models:
            return None
        model_data = models[0]

    return AssociatedModelType(**repo._process_datetime_fields(model_data))


def resolve_associated_model_list(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> AssociatedModelListType:
    repo = AssociatedModelRepo()
    models = repo.list(
        endpoint_id=info.context["endpoint_id"],
        model_uuid=kwargs.get("model_uuid"),
        action_name_contains=kwargs.get("action_name_contains"),
        limit=kwargs.get("limit"),
    )
    model_list = [
        AssociatedModelType(**repo._process_datetime_fields(m)) for m in models
    ]
    return AssociatedModelListType(associated_model_list=model_list, total=len(models))


def insert_update_associated_model(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> AssociatedModelType:
    repo = AssociatedModelRepo()
    endpoint_id = info.context["endpoint_id"]
    if "associated_model_uuid" not in kwargs:
        kwargs["associated_model_uuid"] = f"asc-{etcd_client.new_id()[:8]}"
    key = repo.key(endpoint_id, kwargs["associated_model_uuid"])

    value = dict(
        associated_model_uuid=kwargs["associated_model_uuid"],
        endpoint_id=endpoint_id,
        model_uuid=kwargs["model_uuid"],
        actions=kwargs.get("actions", {}),
        updated_by="system",
    )
    idx_key = k_idx_model_associated(
        kwargs["model_uuid"], kwargs["associated_model_uuid"]
    )
    model_data = repo.upsert(key, value, [idx_key])
    return AssociatedModelType(**repo._process_datetime_fields(model_data))


def delete_associated_model(info: ResolveInfo, **kwargs: Dict[str, Any]) -> bool:
    repo = AssociatedModelRepo()
    endpoint_id = info.context["endpoint_id"]
    associated_model_uuid = kwargs["associated_model_uuid"]
    model_uuid = kwargs["model_uuid"]

    success, blockers = repo.delete_safe(
        endpoint_id, associated_model_uuid, model_uuid=model_uuid
    )
    return success
