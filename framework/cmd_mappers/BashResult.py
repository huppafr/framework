import logging

logger = logging.getLogger(__name__)


class BashResult:
    def __init__(self, cmd: str, output: str, exit_code: int, ip_addr: str):
        self.cmd = cmd
        self.output = output.strip() if isinstance(output, str) else output
        self.exit_code = exit_code
        self.ip_addr = ip_addr

    def is_successful(self) -> bool:
        return self.exit_code == 0

    def is_unsuccessful(self) -> bool:
        return self.exit_code != 0

    def __repr__(self) -> str:
        return f"[{self.ip_addr}] : [{self.cmd}] : [{self.exit_code}] \n{self.output}"

    def __eq__(self, other):
        return (
            isinstance(other, BashResult)
            and self.exit_code == other.exit_code
            and self.output == other.output
        )
