#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from graphene import DateTime, List, ObjectType, String

from silvaengine_dynamodb_base import ListObjectType


class PrimaryKeyMetaType(ObjectType):
    associated_model_uuid = String()
    primary_key_metadata_uuid = String()
    attribute_name = String()
    data_type = String()
    key_type = String()
    endpoint_id = String()
    updated_by = String()
    created_at = DateTime()
    updated_at = DateTime()


class PrimaryKeyMetaListType(ListObjectType):
    primary_key_meta_list = List(PrimaryKeyMetaType)