# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict, List, Optional, Tuple

import pendulum
from graphene import ResolveInfo

from silvaengine_utility import Utility

from ..handlers import etcd_client
from ..types.model_action import ModelActionListType, ModelActionType
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_model_actions(endpoint_id, model_action_uuid):
    return f"{ETCD_PREFIX}/model_actions/{endpoint_id}/{model_action_uuid}"


def k_idx_endpoint_actions(endpoint_id, model_action_uuid):
    return f"{ETCD_PREFIX}/index/by-endpoint/{endpoint_id}/model_actions/{model_action_uuid}"


class ModelActionRepo(BaseRepo):
    def key(self, endpoint_id: str, model_action_uuid: str) -> str:
        return k_model_actions(endpoint_id, model_action_uuid)

    def list(
        self,
        *,
        endpoint_id: Optional[str] = None,
        model_uuid: Optional[str] = None,
        action_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        docs: List[dict] = []
        if endpoint_id:
            # Try index-based lookup first
            ids = [
                k.rsplit("/", 1)[-1]
                for k in etcd_client.iter_keys(
                    f"{ETCD_PREFIX}/index/by-endpoint/{endpoint_id}/model_actions/"
                )
            ]
            for mid in ids:
                doc = etcd_client.get_json(self.key(endpoint_id, mid))
                if doc:
                    docs.append(doc)

            # Fallback to direct prefix scan if index is empty
            if not docs:
                for _k, payload in etcd_client.iter_prefix(
                    f"{ETCD_PREFIX}/model_actions/{endpoint_id}/"
                ):
                    if payload:
                        docs.append(payload)
        else:
            for _k, payload in etcd_client.iter_prefix(f"{ETCD_PREFIX}/model_actions/"):
                if payload:
                    docs.append(payload)

        if model_uuid:
            docs = [d for d in docs if match(d, model_uuid=model_uuid)]
        if action_name:
            docs = [d for d in docs if match(d, action_name=action_name)]
        if limit:
            docs = docs[:limit]
        return docs

    def delete_safe(
        self, endpoint_id: str, model_action_uuid: str
    ) -> Tuple[bool, List[str]]:
        blockers: List[str] = []
        if etcd_client.has_any(f"{ETCD_PREFIX}/model_action_tx/{model_action_uuid}/"):
            blockers.append("Transactions exist for this model action")
        if blockers:
            return False, blockers
        ok = self.delete_key_only(self.key(endpoint_id, model_action_uuid))
        if not ok:
            return False, ["Delete failed"]
        etcd_client.delete_key(k_idx_endpoint_actions(endpoint_id, model_action_uuid))
        return True, []


def resolve_model_action(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> ModelActionType:
    repo = ModelActionRepo()
    model_action_uuid = kwargs.get("model_action_uuid")
    if model_action_uuid:
        # Direct lookup by UUID
        key = repo.key(info.context["endpoint_id"], model_action_uuid)
        action_data = repo.get(key)
        if not action_data:
            return None
    else:
        # List lookup
        actions = repo.list(
            endpoint_id=info.context["endpoint_id"],
            model_uuid=kwargs.get("model_uuid"),
            action_name=kwargs.get("action_name"),
            limit=1,
        )
        if not actions:
            return None
        action_data = actions[0]

    return ModelActionType(**repo._process_datetime_fields(action_data))


def resolve_model_action_list(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> ModelActionListType:
    repo = ModelActionRepo()
    actions = repo.list(
        endpoint_id=info.context["endpoint_id"],
        model_uuid=kwargs.get("model_uuid"),
        action_name=kwargs.get("action_name"),
        limit=kwargs.get("limit"),
    )
    action_list = [ModelActionType(**repo._process_datetime_fields(a)) for a in actions]
    return ModelActionListType(model_action_list=action_list, total=len(actions))


def insert_update_model_action(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> ModelActionType:
    repo = ModelActionRepo()
    endpoint_id = info.context["endpoint_id"]
    if "model_action_uuid" not in kwargs:
        kwargs["model_action_uuid"] = etcd_client.new_id()
    key = repo.key(endpoint_id, kwargs["model_action_uuid"])

    value = dict(
        model_action_uuid=kwargs["model_action_uuid"],
        endpoint_id=endpoint_id,
        model_uuid=kwargs["model_uuid"],
        action_name=kwargs["action_name"],
        associated_model_uuids=kwargs.get("associated_model_uuids", []),
        updated_by="system",
    )
    idx_key = k_idx_endpoint_actions(endpoint_id, kwargs["model_action_uuid"])
    action_data = repo.upsert(key, value, [idx_key])
    return ModelActionType(**repo._process_datetime_fields(action_data))


def delete_model_action(info: ResolveInfo, **kwargs: Dict[str, Any]) -> bool:
    repo = ModelActionRepo()
    endpoint_id = info.context["endpoint_id"]
    model_action_uuid = kwargs["model_action_uuid"]

    success, blockers = repo.delete_safe(endpoint_id, model_action_uuid)
    return success
