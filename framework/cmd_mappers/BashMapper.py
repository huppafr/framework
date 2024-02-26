import logging
from time import sleep

from framework.cmd_mappers.BashResult import BashResult
from framework.cmd_mappers.FioMapper import FioCmdMapper
from framework.ssh_connect.SshConnect import SshConnect

logger = logging.getLogger(__name__)


class AbstractLinuxMapper:
    def __init__(self, ssh_connect: SshConnect) -> None:
        if not isinstance(ssh_connect, SshConnect):
            err_msg = 'ssh_connect is not an instance of SshConnect'
            logger.warning(err_msg)
            raise UserWarning(err_msg)
        self.connect = ssh_connect

    @staticmethod
    def _check_exit_code(result: BashResult) -> BashResult:
        if result.exit_code != 0:
            err_msg = f"Exit status of '{result.cmd}' is '{result.exit_code}'"
            logger.error(err_msg)
        return result

    @staticmethod
    def __add_args(args):
        """
        Unpack args list into string with spaces between values
        """
        return ("{} " * len(args)).format(*args)

    @property
    def fio(self) -> FioCmdMapper:
        return FioCmdMapper(self.connect)

    def exec(self, cmd: str) -> BashResult:
        if cmd.find('create') != -1:
            return self.connect.exec(f'echo y | {cmd}')
        return self.connect.exec(cmd=cmd)

    def async_exec(self, cmd: str) -> int:
        return self.connect.async_exec(cmd)

    def background_exec(self, cmd: str) -> None:
        return self.connect.background_exec(cmd)

    def mkdir(self, *args):
        cmd = f"mkdir {self.__add_args(args)}"
        return self.connect.exec(cmd)

    def reboot(self) -> None:
        self.exec('reboot')
        sleep(10)
        self.connect.close()

    def hard_reset(self) -> None:
        logger.info(f'Hard reset [{self.connect.ip_addr}]')
        cmd = 'echo b > /proc/sysrq-trigger'
        self.background_exec(cmd, silent=False)
        sleep(15)
        self.connect.close()

    def crash(self) -> None:
        logger.info(f'Crash [{self.connect.ip_addr}]')
        self.async_exec('echo c > /proc/sysrq-trigger')
        sleep(15)
        self.connect.close()

    def mount(self, device: str, mountpoint: str) -> BashResult:
        return self.connect.exec(f'mount {device} {mountpoint}')

    def cat(self, file: str) -> BashResult:
        assert file is not None
        return self.connect.exec(f"cat {file}")
