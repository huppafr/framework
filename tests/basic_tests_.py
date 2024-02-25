import pytest

from framework.ssh_connect.SshConnect_utils import connect_to_node
from framework.utils.constants import eracli, node, RAID_NAME, RAID_2_NAME
from framework.utils.disasters import CRASH_TYPES
from framework.utils.drive_utils import (get_drives_used_in_raid,
                                         get_free_drives,
                                         clean_all_drives)
from framework.utils.raid_utils import (get_raid_size,
                                        wait_for_raid_initialization,
                                        wait_for_raid_restriping,
                                        ALL_RAID_LEVELS)
from framework.utils.waiters import sleep


@pytest.fixture(autouse=True)
def cleanup():
    eracli.raid.destroy(_all=True)
    clean_all_drives()
    yield
    eracli.raid.destroy(_all=True)
    clean_all_drives()


def crate_delete_raid_test_():
    assert eracli.raid.create(name=RAID_NAME, level=5, drives=4).is_successful()
    assert eracli.raid.show(name=RAID_NAME).is_successful()

    node.reboot()
    connect_to_node()

    assert eracli.raid.show(name=RAID_NAME).is_successful()
    assert eracli.raid.destroy(name=RAID_NAME).is_successful()
    assert RAID_NAME not in node.exec(f'lsblk | grep {RAID_NAME}').output


def create_2_raids_on_same_disks_test_():
    all_free_drives = get_free_drives()
    drives_for_first_raid = all_free_drives[:5]
    drives_for_second_raid = all_free_drives[:5]

    eracli.raid.create(name=RAID_NAME, level=5, drives=drives_for_first_raid)
    assert eracli.raid.show(name=RAID_NAME).is_successful()

    eracli.raid.create(name=RAID_2_NAME, level=5, drives=drives_for_second_raid)
    assert eracli.raid.show(name=RAID_2_NAME).is_unsuccessful()
    assert RAID_NAME not in node.exec(f'lsblk | grep {RAID_2_NAME}').output


def resize_raid_test_():
    eracli.raid.create(name=RAID_NAME, level=5, drives=5)
    wait_for_raid_initialization(name=RAID_NAME)
    raid_size = get_raid_size(name=RAID_NAME)

    raid_drives = get_drives_used_in_raid(raid_name=RAID_NAME)
    assert len(raid_drives) == 5

    extra_drive = get_free_drives()[-1]
    assert eracli.raid.restripe(
        name=RAID_NAME,
        level=5,
        drives=extra_drive,
        _start=True
    ).is_successful()
    wait_for_raid_restriping(name=RAID_NAME)
    assert eracli.raid.resize(name=RAID_NAME).is_successful()

    raid_drives = get_drives_used_in_raid(raid_name=RAID_NAME)
    assert len(raid_drives) == 6

    raid_size_after_resize = get_raid_size(name=RAID_NAME)
    assert raid_size_after_resize > raid_size


@pytest.mark.parametrize('raid_level', ALL_RAID_LEVELS)
def create_all_raid_types_test_(raid_level: str | int):
    eracli.raid.create(name=RAID_NAME, level=raid_level, drives=8).is_successful()
    assert eracli.raid.show(name=RAID_NAME).is_successful()
    assert RAID_NAME in node.exec(f'lsblk | grep {RAID_NAME}').output


@pytest.mark.parametrize('raid_level', ALL_RAID_LEVELS)
@pytest.mark.parametrize('crash_node', CRASH_TYPES)
def resize_successful_after_crash_test_(raid_level: str | int, crash_node: str):
    eracli.raid.create(name=RAID_NAME, level=5, drives=8).is_successful()
    if raid_level != 0:
        wait_for_raid_initialization(name=RAID_NAME)
    raid_size = get_raid_size(name=RAID_NAME)

    raid_drives = get_drives_used_in_raid(raid_name=RAID_NAME)
    assert len(raid_drives) == 8

    extra_drive = get_free_drives()[-1]
    assert eracli.raid.restripe(
        name=RAID_NAME,
        level=raid_level,
        drives=extra_drive,
        _start=True
    ).is_successful()
    wait_for_raid_restriping(name=RAID_NAME)
    assert eracli.raid.resize(name=RAID_NAME).is_successful()
    sleep(10)  # wait a little bit

    raid_drives = get_drives_used_in_raid(raid_name=RAID_NAME)
    assert len(raid_drives) == 9

    raid_size_after_resize = get_raid_size(name=RAID_NAME)
    assert raid_size < raid_size_after_resize

    crash_node()
    connect_to_node()

    raid_drives = get_drives_used_in_raid(raid_name=RAID_NAME)
    assert len(raid_drives) == 9

    raid_size_after_resize = get_raid_size(name=RAID_NAME)
    assert raid_size < raid_size_after_resize


def files_not_corrupted_after_crash_test_():
    eracli.raid.create(name=RAID_NAME, level=5, drives=5)
    wait_for_raid_initialization(name=RAID_NAME)

    raid_dev = f'/dev/era_{RAID_NAME}'
    node.exec(f'mkfs.xfs -f {raid_dev}')

    node.mkdir('/mnt/test_raid')
    node.mount(device=raid_dev, mountpoint='/mnt/test_raid')

    filepath = '/mnt/test_raid/test_file'
    node.fio.write_to_file(filepath=filepath, size_in_mb=100)
    assert node.fio.verify_file(filepath=filepath, size_in_mb=100).is_successful()

    node.crash()
    connect_to_node()

    sleep(10)  # wait a little bit
    node.mount(device=raid_dev, mountpoint='/mnt/test_raid')
    assert node.fio.verify_file(filepath=filepath, size_in_mb=100).is_successful()
