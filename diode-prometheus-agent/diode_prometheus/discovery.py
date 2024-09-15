#!/usr/bin/env python
"""Discover the correct Prometheus Driver."""

import logging

import importlib_metadata
from prometheus import get_network_driver

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prometheus_driver_list() -> list[str]:
    """
    List the available Prometheus drivers.

    This function scans the installed Python packages to identify Prometheus drivers,
    appending their names (with the 'prometheus-' prefix removed and hyphens replaced
    with underscores) to a list of known drivers.

    Returns
    -------
        List[str]: A list of strings representing the names of available Prometheus drivers.
                   The list includes some predefined driver names and dynamically
                   discovered driver names from the installed packages.

    """
    prometheus_packages = ["ios", "eos", "junos", "nxos"]
    prefix = "prometheus-"
    for dist in importlib_metadata.distributions():
        if dist.metadata["Name"].startswith(prefix):
            package = dist.metadata["Name"][len(prefix) :].replace("-", "_")
            prometheus_packages.append(package)
    return prometheus_packages


supported_drivers = prometheus_driver_list()


def set_prometheus_logs_level(level: int):
    """
    Set the logging level for Prometheus and related libraries.

    Args:
    ----
        level (int): The logging level to set. Typically, this can be one of the
                     standard logging levels (e.g., logging.DEBUG, logging.INFO,
                     logging.WARNING, logging.ERROR, logging.CRITICAL).

    This function adjusts the logging levels for the "prometheus", "ncclient","paramiko"
    and "pyeapi" loggers to the specified level, which is useful for controlling the
    verbosity of log output from these libraries.

    """
    logging.getLogger("prometheus").setLevel(level)
    logging.getLogger("ncclient").setLevel(level)
    logging.getLogger("paramiko").setLevel(level)
    logging.getLogger("pyeapi").setLevel(level)


def discover_device_driver(info: dict) -> str:
    """
    Discover the correct Prometheus driver for the given device information.

    Args:
    ----
        info (dict): A dictionary containing device connection information.
            Expected keys are 'hostname', 'username', 'password', 'timeout',
            and 'optional_args'.

    Returns:
    -------
        str: The name of the driver that successfully connects and identifies
             the device. Returns an empty string if no suitable driver is found.

    """
    set_prometheus_logs_level(logging.CRITICAL)
    for driver in supported_drivers:
        try:
            logger.info(f"Hostname {info.hostname}: Trying '{driver}' driver")
            np_driver = get_network_driver(driver)
            with np_driver(
                info.hostname,
                info.username,
                info.password,
                info.timeout,
                info.optional_args,
            ) as device:
                device_info = device.get_facts()
                if device_info.get("serial_number", "Unknown").lower() == "unknown":
                    logger.info(
                        f"Hostname {info.hostname}: '{driver}' driver did not work"
                    )
                    continue
                set_prometheus_logs_level(logging.INFO)
                return driver
        except Exception as e:
            logger.info(
                f"Hostname {info.hostname}: '{driver}' driver did not work. Exception: {str(e)}"
            )
    set_prometheus_logs_level(logging.INFO)
    return ""
