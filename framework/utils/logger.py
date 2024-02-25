import logging
import sys


main_logger = logging.root
main_logger.setLevel(logging.DEBUG)
main_logger.propagate = False

#  This prevents printing tons of INFO messages from Paramiko library
logging.getLogger("paramiko").setLevel(logging.ERROR)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_format = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%H:%M:%S')
stdout_handler.setFormatter(stdout_format)
main_logger.addHandler(stdout_handler)

file_handler = logging.FileHandler(filename='autotests.log')
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_format)
main_logger.addHandler(file_handler)
