#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from graphene import DateTime, List, ObjectType, String

from silvaengine_dynamodb_base import ListObjectType


class ModelType(ObjectType):
    model_uuid = String()
    module_uuid = String()
    model_name = String()
    endpoint_id = String()
    updated_by = String()
    created_at = DateTime()
    updated_at = DateTime()


class ModelListType(ListObjectType):
    model_list = List(ModelType)