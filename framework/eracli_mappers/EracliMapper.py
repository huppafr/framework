from framework.cmd_mappers.CmdBuilder import CmdBuilder
from framework.eracli_mappers.eracli.EracliRaid import EracliRaid
from framework.eracli_mappers.eracli.EracliDrive import EracliDrive
from framework.ssh_connect.SshConnect import SshConnect


class EracliMapper:
    """
    raid                Manage raid settings.
    drive               Manage drive.
    settings            Manage the additional settings of the eracli program.
    """

    def __init__(self, connect: SshConnect) -> None:
        self._connect = connect

    def eracli_command(self) -> CmdBuilder:
        return CmdBuilder()

    def __repr__(self) -> str:
        return f"{self._connect.ip_addr}"

    @property
    def drive(self) -> EracliDrive:
        return EracliDrive(self._connect, self.eracli_command().add('drive'))

    @property
    def raid(self) -> EracliRaid:
        return EracliRaid(self._connect, self.eracli_command().add('raid'))
