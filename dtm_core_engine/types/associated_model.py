#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from graphene import DateTime, List, ObjectType, String

from silvaengine_dynamodb_base import ListObjectType
from silvaengine_utility import JSON


class AssociatedModelType(ObjectType):
    associated_model_uuid = String()
    endpoint_id = String()
    model_uuid = String()
    actions = JSON()
    updated_by = String()
    created_at = DateTime()
    updated_at = DateTime()


class AssociatedModelListType(ListObjectType):
    associated_model_list = List(AssociatedModelType)