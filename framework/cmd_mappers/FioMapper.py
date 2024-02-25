from framework.cmd_mappers.BashResult import BashResult
from framework.ssh_connect.SshConnect import SshConnect


class FioCmdMapper:
    def __init__(self, connect: SshConnect):
        self._connect = connect

    def write_to_file(self, filepath: str, size_in_mb: int) -> BashResult:
        """Writes data to a file at the specified path.

        Args:
            filepath (str): The absolute path to the file for writing.
            size_in_mb (int): The size of the file to write in megabytes.

        Returns:
            BashResult: The result of the FIO command execution.
        """
        cmd = (
            'fio '
            '--rw=write '
            f'--filename={filepath} '
            '--name=file_write_test '
            f'--size={size_in_mb}m '
            '--verify=md5 '
        )
        res = self._connect.exec(cmd)
        return res

    def infinite_write(self, filename: str, runtime_sec: int = 10000) -> None:
        """Starts an infinite write load using FIO.

        Args:
            filename (str): The name of the file or device to write to.
            runtime_sec (int): The duration of the write operation in seconds.
        """
        cmd = (
            'fio '
            '--rw=write '
            f'--filename={filename} '
            '--name=fio_write '
            f'--runtime={runtime_sec} '
            '--time_based'
        )
        self._connect.async_exec(cmd)

    def verify_file(self, filepath: str, size_in_mb: int) -> BashResult:
        """Verifies the integrity of a file written by FIO using the specified hashing algorithm.

        Args:
            filepath (str): The absolute path to the file to verify.
            size_in_mb (int): The size of the file in megabytes, used to define the scope of verification.

        Returns:
            BashResult: The result of the FIO command execution.
        """
        cmd = (
            'fio '
            '--rw=read '
            f'--filename={filepath} '
            '--name=file_verify_test '
            f'--size={size_in_mb}M '
            '--verify=md5 '
            '--verify_fatal=1 '
            '--verify_only'
        )
        res = self._connect.exec(cmd)
        return res
