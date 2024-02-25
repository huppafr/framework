import logging

from typing import Dict, Union, Optional

logger = logging.getLogger(__name__)


class CmdBuilder:
    def __init__(self) -> None:
        self.__cmd = 'eracli'

    def add(self, value: Union[bool, None, str]):
        """
        Adds the string representation of a value to the command string.

        - If the value is None, nothing is added.
        - If the value is a bool, '1' or '0' is added based on its truthiness.

        Args:
            value: The value to be added to the command string.

        Returns:
            The CmdBuilder instance (self) for chaining.
        """
        if value is None:
            return self

        if isinstance(value, bool):
            value = "1" if value else "0"

        self.__cmd += " " + str(value)
        return self

    def add_key(self, key: str, value: str):
        """
        Adds a key-value pair to the command string.

        - If the value is None, nothing is added.
        - If the value is a bool, '1' or '0' is added based on its truthiness.

        Examples:
            - add_key("-raid_level", 10) adds " -raid_level 10"
            - add_key("-affinity", True) adds " -affinity 1"
            - add_key("-optional_param", None) adds nothing

        Args:
            key: The argument key (e.g., "-raid_level").
            value: The argument value.

        Returns:
            The CmdBuilder instance (self) for chaining.
        """
        if not isinstance(key, str):
            error_msg = 'Key expected to be str but got %s', type(key)
            logger.error(error_msg)
            raise Exception(error_msg)

        if value is None:
            return self

        self.add(key).add(value)
        return self

    def add_dict(self, dictionary: Dict):
        """
        Adds each key-value pair from the dictionary to the command string.

        Args:
            dictionary: A dictionary of key-value pairs to be added.

        Returns:
            The CmdBuilder instance (self) for chaining.
        """
        for key, value in dictionary.items():
            self.add_key(key, value)
        return self

    def add_bool(self, key: str, bool_value: Optional[bool]):
        """
        Adds a key to the command string if the boolean value is True.

        This is used for eracli arguments that do not have a value and are either
        present or absent (e.g., "--force").

        Examples:
            - add_bool("-f", True) adds " -f"
            - add_bool("-f", False) does nothing
            - add_bool("-f", None) does nothing

        Args:
            key: The argument key (e.g., "--force").
            bool_value: Determines whether the key should be added.

        Returns:
            The CmdBuilder instance (self) for chaining.
        """
        if bool_value is None:
            return self

        if not isinstance(key, str):
            msg = 'Key expected to be str but actually is %s', type(key)
            logger.debug(msg)
            raise Exception(msg)

        if not isinstance(bool_value, bool):
            msg = 'Value expected to be bool but actually is %s', type(bool_value)
            logger.debug(msg)
            raise Exception(msg)

        if bool_value:
            self.__cmd += " " + key

        return self

    def get(self) -> str:
        return self.__cmd
