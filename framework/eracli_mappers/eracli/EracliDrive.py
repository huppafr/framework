from framework.eracli_mappers.EraSuper import EraSuper


class EracliDrive(EraSuper):
    """
    clean      Delete the metadata and reset the error counter from the drives.
    """

    def clean(self, drives):
        return self._exec(self.eracli_command.add('clean')
                                             .add_key('--drives', drives))
