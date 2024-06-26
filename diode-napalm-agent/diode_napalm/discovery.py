#!/usr/bin/env python
# Copyright 2024 NetBox Labs Inc
"""Discover the correct NAPALM Driver."""

import logging

from napalm import get_network_driver

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

supported_drivers = ["ios", "eos", "junos", "nxos"]


def set_napalm_logs_level(level: int):
    """
    Set the logging level for NAPALM and related libraries.

    Args:
    ----
        level (int): The logging level to set. Typically, this can be one of the
                     standard logging levels (e.g., logging.DEBUG, logging.INFO,
                     logging.WARNING, logging.ERROR, logging.CRITICAL).

    This function adjusts the logging levels for the "napalm", "ncclient","paramiko"
    and "pyeapi" loggers to the specified level, which is useful for controlling the
    verbosity of log output from these libraries.

    """
    logging.getLogger("napalm").setLevel(level)
    logging.getLogger("ncclient").setLevel(level)
    logging.getLogger("paramiko").setLevel(level)
    logging.getLogger("pyeapi").setLevel(level)


def discover_device_driver(info: dict) -> str:
    """
    Discover the correct NAPALM driver for the given device information.

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
    set_napalm_logs_level(logging.CRITICAL)
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
                set_napalm_logs_level(logging.INFO)
                return driver
        except Exception as e:
            logger.info(
                f"Hostname {info.hostname}: '{driver}' driver did not work. Exception: {str(e)}"
            )
    set_napalm_logs_level(logging.INFO)
    return ""
