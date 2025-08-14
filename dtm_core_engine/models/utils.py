# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

ETCD_PREFIX = "/dtm/v1"


def match(doc: dict, **criteria) -> bool:
    """
    Light filtering ops:
      - field="x" (exact)
      - field__contains="x" (substring for strings, membership for lists)
      - field__in=[a,b,c]
      - field__neq="x"
    Missing fields ⇒ False except __neq (treated as not equal).
    """
    for key, expected in criteria.items():
        if "__" in key:
            field, op = key.split("__", 1)
        else:
            field, op = key, "eq"
        val = doc.get(field, None)

        if op == "eq":
            if val != expected:
                return False
        elif op == "neq":
            if val == expected:
                return False
        elif op == "contains":
            if isinstance(val, str):
                if not isinstance(expected, str) or expected not in val:
                    return False
            elif isinstance(val, list):
                if expected not in val:
                    return False
            else:
                return False
        elif op == "in":
            if val not in expected:
                return False
        else:
            return False
    return True
