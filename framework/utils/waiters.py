import time

from framework.utils.logger import main_logger as logger


def sleep(wait_time: int = 2, description: str = '') -> None:
    logger.info(description)
    time.sleep(wait_time)


def wait_for(
    expected,
    wait_time: int = 1000,
    polling: int = 2,
) -> bool:
    """
    Waits for 'expected' condition to be true within 'wait_time', polling every 'polling' seconds.

    Args:
        expected (Callable): Function to evaluate the condition.
        wait_time (int): Max time to wait in seconds. Default is 1000.
        polling (int): Time between checks in seconds. Default is 2.

    Returns:
        bool: True if 'expected' becomes true within 'wait_time', else False.
    """
    result = 0
    num_of_try = 0
    start_time = time.time()
    result = time.time() - start_time
    while result < wait_time:
        num_of_try += 1
        try:
            if expected():
                logger.info(f'Waiting ended in {result:.2f} seconds')
                return True
            else:
                if result > wait_time:
                    logger.warning("Waiting time is up!")
                    return False
                time.sleep(polling)
                result = time.time() - start_time
        except Exception as exp:
            logger.error(exp)
        if num_of_try % 10 == 0:
            try:
                from framework.ssh_connect.SshConnect_utils import connect_to_node
                from framework.utils.constants import node
                node.connect.close()
                connect_to_node()
            except Exception as e:
                logger.debug(e)
