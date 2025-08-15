# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import logging
from typing import Any, Dict


class Config:
    """
    Centralized Configuration Class
    Manages shared configuration variables across the DTM Core Engine application.
    """

    etcd_host = "127.0.0.1"
    etcd_port = 2379

    @classmethod
    def initialize(cls, logger: logging.Logger, **setting: Dict[str, Any]) -> None:
        """
        Initialize configuration setting.
        Args:
            logger (logging.Logger): Logger instance for logging.
            **setting (Dict[str, Any]): Configuration dictionary.
        """
        try:
            cls.etcd_host = setting.get("etcd_host", "127.0.0.1")
            cls.etcd_port = setting.get("etcd_port", 2379)
            logger.info("DTM Core Engine configuration initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize DTM Core Engine configuration.")
            raise e
