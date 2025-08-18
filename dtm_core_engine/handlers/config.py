# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import logging
from typing import Any, Dict

import boto3


class Config:
    """
    Centralized Configuration Class
    Manages shared configuration variables across the DTM Core Engine application.
    """

    etcd_host = "127.0.0.1"
    etcd_port = 2379
    package_bucket_name = None
    package_zip_path = None
    package_extract_path = None
    aws_s3 = None

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
            cls.package_bucket_name = setting.get("package_bucket_name", None)
            cls.package_zip_path = setting.get("package_zip_path", "/tmp/package_zips")
            cls.package_extract_path = setting.get(
                "package_extract_path", "/tmp/packages"
            )
            cls._initialize_aws_services(setting)
            logger.info("DTM Core Engine configuration initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize DTM Core Engine configuration.")
            raise e

    @classmethod
    def _initialize_aws_services(cls, setting: Dict[str, Any]) -> None:
        """
        Initialize AWS services, such as the S3 client.
        Args:
            setting (Dict[str, Any]): Configuration dictionary.
        """
        if all(
            setting.get(k)
            for k in ["region_name", "aws_access_key_id", "aws_secret_access_key"]
        ):
            aws_credentials = {
                "region_name": setting["region_name"],
                "aws_access_key_id": setting["aws_access_key_id"],
                "aws_secret_access_key": setting["aws_secret_access_key"],
            }
        else:
            aws_credentials = {}

        cls.aws_s3 = boto3.client(
            "s3",
            **aws_credentials,
            config=boto3.session.Config(signature_version="s3v4"),
        )
