#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from graphene import DateTime, List, ObjectType, String

from silvaengine_dynamodb_base import ListObjectType


class ModuleType(ObjectType):
    endpoint_id = String()
    module_uuid = String()
    module_name = String()
    package_name = String()
    data_source_uuid = String()
    source = String()
    updated_by = String()
    created_at = DateTime()
    updated_at = DateTime()


class ModuleListType(ListObjectType):
    module_list = List(ModuleType)