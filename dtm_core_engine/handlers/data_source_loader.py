# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import logging
from typing import Dict, List, Optional

from silvaengine_utility import Utility

from .dtm_utility import get_class
from .inquiry import InquiryHandler


class DataSourceLoader:
    """
    Data Source Loader
    Manages loading and caching of data sources for the DTM Core Engine.
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self._cache: Dict[str, dict] = {}

    def load_all_data_sources(self, endpoint_id: str) -> List[dict]:
        """
        Load all data sources for a given endpoint.

        Args:
            endpoint_id (str): The endpoint identifier

        Returns:
            List[dict]: List of all data sources
        """
        try:
            data_sources = InquiryHandler.list_data_sources(endpoint_id)
            self.logger.info(
                f"Loaded {len(data_sources)} data sources for endpoint {endpoint_id}"
            )
            return data_sources
        except Exception as e:
            self.logger.error(
                f"Failed to load data sources for endpoint {endpoint_id}: {e}"
            )
            return []

    def get_data_source(
        self, endpoint_id: str, data_source_uuid: str
    ) -> Optional[dict]:
        """
        Get a specific data source by UUID.

        Args:
            endpoint_id (str): The endpoint identifier
            data_source_uuid (str): The data source UUID

        Returns:
            Optional[dict]: Data source data or None if not found
        """
        cache_key = f"{endpoint_id}:{data_source_uuid}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            self.refresh_cache(endpoint_id)
            return self._cache[cache_key]
        except Exception as e:
            self.logger.error(f"Failed to get data source {data_source_uuid}: {e}")
            return None

    def refresh_cache(self, endpoint_id: str) -> None:
        """
        Refresh the data source cache for an endpoint.

        Args:
            endpoint_id (str): The endpoint identifier
        """
        try:
            # Clear existing cache for this endpoint
            # keys_to_remove = [
            #     k for k in self._cache.keys() if k.startswith(f"{endpoint_id}:")
            # ]
            # for key in keys_to_remove:
            #     del self._cache[key]

            # Reload all data sources
            data_sources = self.load_all_data_sources(endpoint_id)
            for ds in data_sources:
                cache_key = f"{endpoint_id}:{ds['data_source_uuid']}"
                if ds.get("connector_module_name") and ds.get("connector_class_name"):
                    connector_class = get_class(
                        ds["connector_module_name"],
                        ds["connector_class_name"],
                        package_name=ds["connector_package_name"],
                    )
                    connector = connector_class(
                        self.logger,
                        **Utility.json_loads(Utility.json_dumps(ds["setting"])),
                    )
                    self._cache[cache_key] = dict(
                        ds["setting"], **{"connector": connector}
                    )
                    continue

                self._cache[cache_key] = ds["setting"]

            self.logger.info(f"Refreshed data source cache for endpoint {endpoint_id}")
        except Exception as e:
            self.logger.error(f"Failed to refresh data source cache: {e}")
