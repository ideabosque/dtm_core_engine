#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from graphene import DateTime, List, ObjectType, String

from silvaengine_dynamodb_base import ListObjectType
from silvaengine_utility import JSON


class ModelActionTxType(ObjectType):
    model_action_uuid = String()
    transaction_uuid = String()
    endpoint_id = String()
    associated_model_uuid = String()
    primary_key = JSON()
    arguments = JSON()
    status = String()
    notes = String()
    updated_by = String()
    created_at = DateTime()
    updated_at = DateTime()


class ModelActionTxListType(ListObjectType):
    model_action_tx_list = List(ModelActionTxType)