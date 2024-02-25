import logging
import os
import subprocess
import time

import paramiko

from framework.ssh_connect.SshConnect import SshConnect
from framework.utils.parse_config import parse_properties

logger = logging.getLogger(__name__)


def connect_to_node() -> SshConnect:
    """
    Establishes an SSH connection to a node using credentials and IP address
    obtained from the node's configuration properties.

    Returns:
        SshConnect: An established SSH connection to the node.

    Raises:
        TimeoutError: If the node does not become available within the timeout period.
    """
    node_info = parse_properties()
    add_host_key(node_info['node_IP'])

    timeout = 120
    start_time = time.time()

    while True:
        try:
            connect = SshConnect(node_info['node_IP'], node_info['node_user'], node_info['node_pass'])
            logger.info("Connected to %s", node_info['node_IP'])
            return connect
        except (paramiko.ssh_exception.SSHException,
                paramiko.ssh_exception.NoValidConnectionsError,
                ConnectionResetError,
                TimeoutError) as error:
            if time.time() - start_time > timeout:
                logger.error("Timeout waiting for node '%s' to become available.", node_info['node_IP'])
                raise TimeoutError(f"Timeout waiting for node '{node_info['node_IP']}' to become available.")
            logger.debug("Node '%s' not available yet, retrying...", node_info['node_IP'])
            time.sleep(5)


def add_host_key(ip: str) -> None:
    """
    Adds the host key of the given IP address to the known_hosts file to avoid
    SSH connection warnings. If the key already exists, it is first removed to
    ensure that the updated key is added.

    Args:
        ip (str): The IP address of the host for which the SSH key is to be added.
    """
    known_hosts_exp = os.path.expanduser('~/.ssh/known_hosts')
    subprocess.call(['ssh-keygen', '-f', known_hosts_exp, '-R', ip])

    try:
        with open(known_hosts_exp, 'a') as known_hosts_stream:
            subprocess.call(['ssh-keyscan', '-H', ip], stdout=known_hosts_stream)
    except FileNotFoundError as err:
        logger.error('known_hosts file is not found!\n')
        logger.debug(err)
