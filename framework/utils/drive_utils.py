import logging
import re
from typing import List

from framework.utils.constants import eracli, node

logger = logging.getLogger(__name__)


def get_free_drives() -> List[str]:
    """
    Retrieves a list of free drives that are not used in any RAID and are not system drives.

    :return: List of free drives.
    """
    exclude_drives = set(get_drives_used_in_raid() + get_system_drive())
    res = node.exec('lsblk').output.split('\n')
    free_drives = [line.split(' ')[0] for line in res if line.startswith('sd') and line.split(' ')[0] not in exclude_drives]

    return free_drives


def get_drives_used_in_raid(raid_name: str = None) -> List[str]:
    """
    Retrieves a list of drives used in a specific RAID array.

    :param raid_name: Name of the RAID. If None, drives from all RAIDs are returned.
    :return: List of drives used in RAID.
    """
    used_drives = []
    res = eracli.raid.show(name=raid_name)
    if res.is_unsuccessful():
        logger.debug('Raid with name %s not found.', raid_name)
        return used_drives

    for raid in res.body.values():
        used_drives.extend(device[1] for device in raid.get('devices', []))
    return used_drives


def get_system_drive() -> List[str]:
    """
    Retrieves a list of system drives.

    :return: List of system drives.
    """
    res = node.exec('df').output
    sys_drives = set(re.sub(r'\d+$', '', match.split('/')[-1]) for match in re.findall(r'/dev/sd[a-z]+', res))

    return list(sys_drives)
