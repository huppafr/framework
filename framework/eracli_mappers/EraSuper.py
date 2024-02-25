import copy
import json

from framework.cmd_mappers.BashMapper import BashResult
from framework.cmd_mappers.CmdBuilder import CmdBuilder
from framework.ssh_connect.SshConnect import SshConnect


class EraSuper:
    def __init__(self, connect: SshConnect, cmdbuilder: CmdBuilder):
        self._connect = connect
        self._cmdbuilder = cmdbuilder

    def _exec(self, cmd_builder: CmdBuilder):
        assert isinstance(cmd_builder, CmdBuilder)
        res = self._connect.exec(cmd_builder.get())
        if res.cmd.find('--format json') != -1 and len(res.output) != 0:
            res.output = json.loads(res.output)
        else:
            res.output

        return BashResult(res.cmd, res.output, res.exit_code, res.ip_addr)

    @property
    def eracli_command(self) -> CmdBuilder:
        return copy.deepcopy(self._cmdbuilder)
