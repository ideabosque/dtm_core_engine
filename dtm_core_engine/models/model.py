# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict, List, Optional, Tuple

from graphene import ResolveInfo

from ..handlers import etcd_client
from ..types.model import ModelListType, ModelType
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_models(module_uuid, model_uuid):
    return f"{ETCD_PREFIX}/models/{module_uuid}/{model_uuid}"


class ModelRepo(BaseRepo):
    def key(self, module_uuid: str, model_uuid: str) -> str:
        return k_models(module_uuid, model_uuid)

    def list(
        self,
        *,
        module_uuid: Optional[str] = None,
        model_name: Optional[str] = None,
        endpoint_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        prefix = (
            f"{ETCD_PREFIX}/models/{module_uuid}/"
            if module_uuid
            else f"{ETCD_PREFIX}/models/"
        )
        results: List[dict] = []
        for _k, payload in self._iter_prefix(prefix):
            if not payload:
                continue
            if model_name and not match(payload, model_name__contains=model_name):
                continue
            if endpoint_id and not match(payload, endpoint_id=endpoint_id):
                continue
            results.append(payload)
            if limit and len(results) >= limit:
                break
        return results

    def delete_safe(self, module_uuid: str, model_uuid: str) -> Tuple[bool, List[str]]:
        blockers: List[str] = []
        if etcd_client.has_any(
            f"{ETCD_PREFIX}/index/by-model/{model_uuid}/associated/"
        ):
            blockers.append("Associated models exist for this model")
        for _k, doc in etcd_client.iter_prefix(f"{ETCD_PREFIX}/model_actions/"):
            if doc and doc.get("model_uuid") == model_uuid:
                blockers.append(
                    f"ModelAction {doc.get('model_action_uuid')} references this model"
                )
                break
        if blockers:
            return False, blockers
        ok = self.delete_key_only(self.key(module_uuid, model_uuid))
        return ok, ([] if ok else ["Delete failed"])


def resolve_model(info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModelType:
    repo = ModelRepo()
    model_uuid = kwargs.get("model_uuid")
    module_uuid = kwargs.get("module_uuid")  # Required by schema

    if model_uuid and module_uuid:
        # Direct lookup by both UUIDs
        key = repo.key(module_uuid, model_uuid)
        model_data = repo.get(key)
        if not model_data:
            return None
        return ModelType(**repo._process_datetime_fields(model_data))
    else:
        # List lookup by module_uuid and optional model_name
        models = repo.list(
            module_uuid=module_uuid,
            model_name=kwargs.get("model_name"),
            endpoint_id=info.context["endpoint_id"],
            limit=1,
        )
        if not models:
            return None
        return ModelType(**repo._process_datetime_fields(models[0]))


def resolve_model_list(info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModelListType:
    repo = ModelRepo()
    models = repo.list(
        module_uuid=kwargs.get("module_uuid"),
        model_name=kwargs.get("model_name"),
        endpoint_id=info.context["endpoint_id"],
        limit=kwargs.get("limit"),
    )
    model_list = [ModelType(**repo._process_datetime_fields(m)) for m in models]
    return ModelListType(model_list=model_list, total=len(models))


def insert_update_model(info: ResolveInfo, **kwargs: Dict[str, Any]) -> ModelType:
    repo = ModelRepo()
    if "model_uuid" not in kwargs:
        kwargs["model_uuid"] = f"mdl-{etcd_client.new_id()[:8]}"
    key = repo.key(kwargs["module_uuid"], kwargs["model_uuid"])

    value = dict(
        model_uuid=kwargs["model_uuid"],
        module_uuid=kwargs["module_uuid"],
        model_name=kwargs.get("model_name", "Order"),
        endpoint_id=info.context["endpoint_id"],
        updated_by="system",
    )
    model_data = repo.upsert(key, value)
    return ModelType(**repo._process_datetime_fields(model_data))


def delete_model(info: ResolveInfo, **kwargs: Dict[str, Any]) -> bool:
    repo = ModelRepo()
    module_uuid = kwargs["module_uuid"]
    model_uuid = kwargs["model_uuid"]

    success, blockers = repo.delete_safe(module_uuid, model_uuid)
    return success
