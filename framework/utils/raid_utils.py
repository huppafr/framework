from framework.utils.constants import eracli
from framework.utils.waiters import wait_for

ALL_RAID_LEVELS = [0, 1, 10, 5, 6, 7, 50, 60, 70]


def get_raid_size(name: str) -> int:
    res = eracli.raid.show(name=name).output
    try:
        size = res.get(name)['size'].split()[0]
    except AttributeError:
        err_msg = (f'RAID {name} was not found. '
                   'Check the name of the RAID and check if the raid exists.')
        assert False, err_msg
    return int(size)


def get_raid_states(name: str) -> str:
    return eracli.raid.show(name=name).output.get(name).get('state')


def wait_for_raid_initialization(name: str):
    states = ['online', 'initialized']
    wait_for(
        lambda: get_raid_states(name=name) == states,
        wait_time=1000
    )


def wait_for_raid_restriping(name: str):
    states = ['online', 'initialized', 'need_resize']
    wait_for(
        lambda: get_raid_states(name=name) == states,
        wait_time=1000
    )
