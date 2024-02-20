import logging
import re
from typing import List

from framework.utils.constants import eracli, node

logger = logging.getLogger(__name__)


def get_free_drives() -> List[str]:
    """
    Retrieves a list of free drives that are not used in any RAID configuration
    and are not system drives.

    Returns:
        List[str]: A list of identifiers for the free drives.
    """
    exclude_drives = set(get_drives_used_in_raid() + get_system_drive())
    res = node.exec('lsblk').output.split('\n')
    free_drives = [
        line.split(' ')[0] for line in res
        if line.startswith('sd') and line.split(' ')[0] not in exclude_drives
    ]

    return free_drives


def get_drives_used_in_raid(raid_name: str = None) -> List[str]:
    """
    Retrieves a list of drives used in a specific RAID array or in all RAIDs
    if no name is provided.

    Args:
        raid_name (str, optional): The name of the RAID. If None, drives
        from all RAID arrays are returned.

    Returns:
        List[str]: A list of identifiers for the drives used in the specified RAID(s).
    """
    used_drives = []
    res = eracli.raid.show(name=raid_name)
    if res.is_unsuccessful():
        logger.debug('Raid with name %s not found.', raid_name)
        return used_drives

    if len(res.output) == 0:
        return used_drives

    for key, value in res.output.items():
        used_drives.extend(
            device[1] for device in value.get('devices', [])
        )

    return used_drives


def get_system_drive() -> List[str]:
    """
    Retrieves a list of system drives.

    Returns:
        List[str]: A list of identifiers for the system drives.
    """
    res = node.exec('df').output
    sys_drives = set(
        re.sub(r'\d+$', '', match.split('/')[-1])
        for match in re.findall(r'/dev/sd[a-z]+', res)
    )

    return list(sys_drives)
