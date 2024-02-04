import logging
import time
import paramiko

from framework.cmd_mappers.BashResult import BashResult

logger = logging.getLogger(__name__)


class SshConnect:
    def __init__(self, ip_addr: str, user: str, password: str, port: int = 22):
        """
        Initialize an SSH connection to a remote server.

        Args:
            ip_addr (str): IP address or hostname of the remote server.
            user (str): Username for authentication on the remote server.
            password (str): Password for authentication on the remote server.
            port (int): SSH port on the remote server (defaults to 22).
        """
        self.ip_addr = ip_addr
        self.__client = paramiko.SSHClient()
        self.__client.load_system_host_keys()
        self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__client.connect(
            hostname=ip_addr,
            username=user,
            password=password,
            port=port,
            timeout=300
        )

    def exec(self, cmd: str, ignore_stderr: bool = True) -> BashResult:
        """
        Execute a command on the remote server over SSH.

        Args:
            cmd (str): The command to execute on the remote server.
            ignore_stderr (bool): If True, the standard error stream (stderr) will be ignored.
                                  If False, the content of stderr will be appended to the command output.

        Returns:
            BashResult: An instance of BashResult containing the command output, exit status, and server IP address.
        """
        logger.info(f'{self.ip_addr} cmd: {cmd}')
        start_time = time.time()

        stdin, stdout, stderr = self.__client.exec_command(cmd)
        cmd_output = stdout.read().decode('utf-8')
        if not ignore_stderr:
            cmd_error = stderr.read().decode('utf-8')
            cmd_output += cmd_error

        exit_status = stdout.channel.recv_exit_status()
        logger.info(
            f'cmd exit code: {exit_status}. Run time: {time.time() - start_time:.2f} s \n\n'
            f'{cmd_output.encode("ascii", "ignore").decode("utf-8")}'
        )
        return BashResult(cmd, cmd_output, exit_status, self.ip_addr)
