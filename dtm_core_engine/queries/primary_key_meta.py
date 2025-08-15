#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from typing import Any, Dict

from graphene import ResolveInfo

from ..models import primary_key_meta
from ..types.primary_key_meta import PrimaryKeyMetaListType, PrimaryKeyMetaType


def resolve_primary_key_meta(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> PrimaryKeyMetaType:
    return primary_key_meta.resolve_primary_key_meta(info, **kwargs)


def resolve_primary_key_meta_list(
    info: ResolveInfo, **kwargs: Dict[str, Any]
) -> PrimaryKeyMetaListType:
    return primary_key_meta.resolve_primary_key_meta_list(info, **kwargs)
