import logging

logger = logging.getLogger(__name__)


class BashResult:
    def __init__(self, cmd: str, output: str, exit_code: int, ip_addr: str) -> None:
        """
        Initialize a BashResult instance.

        Args:
            cmd (str): Command executed.
            output (str): Output produced by the command.
            exit_code (int): Exit code returned by the command.
            ip_addr (str): IP address of the target where command was executed.
        """
        self.cmd = cmd
        self.output = output.strip()
        self.exit_code = exit_code
        self.ip_addr = ip_addr

    def is_successful(self) -> bool:
        return self.exit_code == 0

    def is_unsuccessful(self) -> bool:
        return self.exit_code != 0

    def __repr__(self) -> str:
        return f'[{self.ip_addr}] : [{self.cmd}] : [{self.exit_code}]' f'\n{self.output}'

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, BashResult)
            and self.exit_code == other.exit_code
            and self.output == other.output
        )
