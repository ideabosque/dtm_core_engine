# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import logging
import os
import sys
import traceback
import zipfile
from typing import Optional

from .config import Config


def module_exists(logger: logging.Logger, module_name: str) -> bool:
    """Check if the module exists in the specified path."""
    module_dir = os.path.join(Config.package_extract_path, module_name)
    if os.path.exists(module_dir) and os.path.isdir(module_dir):
        logger.info(f"Module {module_name} found in {Config.package_extract_path}.")
        return True
    logger.info(f"Module {module_name} not found in {Config.package_extract_path}.")
    return False


def download_and_extract_module(
    logger: logging.Logger, module_name: str, package_name: str = None
) -> None:
    """Download and extract the module from S3 if not already extracted."""
    key = f"{module_name}.zip" if package_name is None else f"{package_name}.zip"
    zip_path = f"{Config.package_zip_path}/{key}"

    logger.info(
        f"Downloading module from S3: bucket={Config.package_bucket_name}, key={key}"
    )
    Config.aws_s3.download_file(Config.package_bucket_name, key, zip_path)
    logger.info(f"Downloaded {key} from S3 to {zip_path}")

    # Extract the ZIP file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(Config.package_extract_path)
    logger.info(f"Extracted module to {Config.package_extract_path}")


def get_class(
    logger: logging.Logger, module_name: str, class_name: str, package_name: str = None
) -> Optional[type]:
    try:
        # Check if the module exists
        if not module_exists(module_name):
            # Download and extract the module if it doesn't exist
            download_and_extract_module(module_name, package_name=package_name)

        # Add the extracted module to sys.path
        module_path = f"{Config.package_extract_path}/{module_name}"
        if module_path not in sys.path:
            sys.path.append(module_path)

        # Import the module and get the class
        module = __import__(module_name)
        return getattr(module, class_name)
    except Exception as e:
        log = traceback.format_exc()
        logger.error(log)
        raise e
