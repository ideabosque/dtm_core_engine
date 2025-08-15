#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from graphene import DateTime, List, ObjectType, String

from silvaengine_dynamodb_base import ListObjectType
from silvaengine_utility import JSON


class AssociatedModelActionType(ObjectType):
    transaction_uuid = String()
    action_name = String()
    model_action_uuid = String()
    status = String()
    response = JSON()
    notes = String()
    updated_by = String()
    created_at = DateTime()
    updated_at = DateTime()


class AssociatedModelActionListType(ListObjectType):
    associated_model_action_list = List(AssociatedModelActionType)