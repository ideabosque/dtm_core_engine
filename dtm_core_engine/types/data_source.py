#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from graphene import DateTime, List, ObjectType, String

from silvaengine_dynamodb_base import ListObjectType
from silvaengine_utility import JSON


class DataSourceType(ObjectType):
    endpoint_id = String()
    data_source_uuid = String()
    data_source_name = String()
    setting = JSON()
    connector_class_name = String()
    connector_module_name = String()
    connector_package_name = String()
    updated_by = String()
    created_at = DateTime()
    updated_at = DateTime()


class DataSourceListType(ListObjectType):
    data_source_list = List(DataSourceType)
