from framework.cmd_mappers.BashMapper import AbstractLinuxMapper
from framework.eracli_mappers.EracliMapper import EracliMapper
from framework.ssh_connect.SshConnect_utils import connect_to_node
from framework.utils.parse_config import parse_properties

connection = connect_to_node()
node = AbstractLinuxMapper(connection)
eracli = EracliMapper(connection)

PROPS = parse_properties()
RAID_NAME = 'test_raid'
RAID_2_NAME = 'test_raid2'
