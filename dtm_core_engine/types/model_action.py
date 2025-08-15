#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from graphene import DateTime, List, ObjectType, String

from silvaengine_dynamodb_base import ListObjectType


class ModelActionType(ObjectType):
    model_action_uuid = String()
    endpoint_id = String()
    model_uuid = String()
    action_name = String()
    associated_model_uuids = List(String)
    updated_by = String()
    created_at = DateTime()
    updated_at = DateTime()


class ModelActionListType(ListObjectType):
    model_action_list = List(ModelActionType)