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
        self.user = user
        self.password = password
        self.port = port
        self.__client = None
        self.__setup_client()

    def __setup_client(self):
        """
        Sets up the SSH client with host keys and connection policy.
        """
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__client = client

    def ensure_connection(self, timeout=120, retry_interval=5):
        """
        Ensures that the SSH connection is established. If the connection
        is not active, it attempts to reconnect within the given timeout.

        Args:
            timeout (int): The total time (in seconds) to attempt reconnection.
            retry_interval (int): The time interval (in seconds) between retries.
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.__client.get_transport() and self.__client.get_transport().is_active():
                return
            try:
                self.__setup_client()
                self.__client.connect(hostname=self.ip_addr, username=self.user,
                                      password=self.password, port=self.port, timeout=retry_interval)
                logger.info('Successfully connected to %s', self.ip_addr)
                return
            except Exception as e:
                logger.debug('Connection failed: %s. Retrying...', e)
                time.sleep(retry_interval)

        raise TimeoutError(f'Failed to connect to {self.ip_addr} within {timeout} seconds.')

    def exec(self, cmd: str, ignore_stderr: bool = True) -> BashResult:
        """
        Execute a command on the remote server over SSH.

        Args:
            cmd (str): The command to execute on the remote server.
            ignore_stderr (bool): If True, ignore the standard error stream.
                                  If False, append stderr to the command output.

        Returns:
            BashResult: An instance containing the command output, exit status,
                        and server IP address.
        """
        self.ensure_connection()
        logger.info("[%s] cmd: [%s]", self.ip_addr, cmd)
        start_time = time.time()

        stdin, stdout, stderr = self.__client.exec_command(cmd)
        cmd_output = stdout.read().decode('utf-8')
        if not ignore_stderr:
            cmd_error = stderr.read().decode('utf-8')
            cmd_output += cmd_error

        exit_status = stdout.channel.recv_exit_status()
        logger.info(f'cmd exit code: {exit_status}. Run time: '
                    f'{time.time() - start_time:.2f} s \n\n'
                    f'{cmd_output.encode("ascii", "ignore").decode("utf-8")}')

        return BashResult(cmd, cmd_output, exit_status, self.ip_addr)

    def async_exec(self, cmd: str) -> int:
        """
        Execute a command on the remote server over SSH without waiting for
        the output. The command is executed in the background.

        Args:
            cmd (str): The command to be executed on the remote server.

        Returns:
            int: The PID of the background command process.
        """
        self.ensure_connection()
        _, stdout, _ = self.__client.exec_command(f'{cmd} & echo $!')
        pid = int(stdout.readline().rstrip())
        logger.info('[%s] async %s [PID: %s]', self.ip_addr, cmd, pid)
        return pid

    def background_exec(self, cmd: str) -> None:
        """
        Sends a command for execution without waiting for a response.

        Args:
            cmd (str): The command to be sent for execution.

        Returns:
            None
        """
        transport = self.__client.get_transport()
        transport.set_keepalive(15)
        session = transport.open_session()
        logger.info("[%s] cmd: [%s]", self.ip_addr, cmd)
        session.exec_command(cmd)

    def close(self):
        """
        Closes the SSH connection.
        """
        if self.__client:
            self.__client.close()
