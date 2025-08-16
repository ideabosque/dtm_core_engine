# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict, List, Optional, Tuple

from graphene import ResolveInfo

from ..types.associated_model_action import (
    AssociatedModelActionListType,
    AssociatedModelActionType,
)
from .base import BaseRepo
from .utils import ETCD_PREFIX, match


def k_associated_actions(transaction_uuid, action_name):
    return f"{ETCD_PREFIX}/associated_model_actions/{transaction_uuid}/{action_name}"


class AssociatedModelActionRepo(BaseRepo):
    def key(self, transaction_uuid: str, action_name: str) -> str:
        return k_associated_actions(transaction_uuid, action_name)

    def list(
        self,
        *,
        transaction_uuid: Optional[str] = None,
        status: Optional[str] = None,
        action_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        docs: List[dict] = []
        if transaction_uuid:
            for _k, payload in self._iter_prefix(
                f"{ETCD_PREFIX}/associated_model_actions/{transaction_uuid}/"
            ):
                if payload:
                    docs.append(payload)
        else:
            for _k, payload in self._iter_prefix(
                f"{ETCD_PREFIX}/associated_model_actions/"
            ):
                if payload:
                    docs.append(payload)
        if status:
            docs = [d for d in docs if match(d, status=status)]
        if action_name:
            docs = [d for d in docs if match(d, action_name=action_name)]
        if limit:
            docs = docs[:limit]
        return docs

    def delete_safe(
        self, transaction_uuid: str, action_name: str
    ) -> Tuple[bool, List[str]]:
        ok = self.delete_key_only(self.key(transaction_uuid, action_name))
        return ok, ([] if ok else ["Delete failed"])


def resolve_associated_model_action(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> AssociatedModelActionType:
    repo = AssociatedModelActionRepo()
    actions = repo.list(
        transaction_uuid=kwargs.get("transaction_uuid"),
        status=kwargs.get("status"),
        action_name=kwargs.get("action_name"),
        limit=1,
    )
    if not actions:
        return None
    return AssociatedModelActionType(**repo._process_datetime_fields(actions[0]))


def resolve_associated_model_action_list(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> AssociatedModelActionListType:
    repo = AssociatedModelActionRepo()
    actions = repo.list(
        transaction_uuid=kwargs.get("transaction_uuid"),
        status=kwargs.get("status"),
        action_name=kwargs.get("action_name"),
        limit=kwargs.get("limit"),
    )
    action_list = [
        AssociatedModelActionType(**repo._process_datetime_fields(a)) for a in actions
    ]
    return AssociatedModelActionListType(
        associated_model_action_list=action_list, total=len(actions)
    )


def insert_update_associated_model_action(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> AssociatedModelActionType:
    repo = AssociatedModelActionRepo()
    key = repo.key(kwargs["transaction_uuid"], kwargs["action_name"])

    value = dict(
        transaction_uuid=kwargs["transaction_uuid"],
        action_name=kwargs["action_name"],
        model_action_uuid=kwargs["model_action_uuid"],
        status=kwargs.get("status", "NEW"),
        response=kwargs.get("response") or {},
        notes=kwargs.get("notes", ""),
        updated_by="worker-1",
    )
    action_data = repo.upsert(key, value)
    return AssociatedModelActionType(**repo._process_datetime_fields(action_data))


def delete_associated_model_action(info: ResolveInfo, **kwargs: Dict[str, Any]) -> bool:
    repo = AssociatedModelActionRepo()
    transaction_uuid = kwargs["transaction_uuid"]
    action_name = kwargs["action_name"]

    success, blockers = repo.delete_safe(transaction_uuid, action_name)
    return success
