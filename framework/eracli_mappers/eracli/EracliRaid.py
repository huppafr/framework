from framework.eracli_mappers.EraSuper import EraSuper


class EracliRaid(EraSuper):
    """
    create              Create the RAID.
    destroy             Delete the RAID without possibility to restore the RAID and data on it.
    modify              Modify the parameters of the created RAID.
    resize              Change the RAID size.
    restripe            Manage the RAID restripe.
    show                Show info about the RAID.
    """

    def create(
        self,
        drives,
        level,
        name,
        sparepool=None,
        synd_cnt=None,
    ):
        from framework.utils.drive_utils import get_free_drives
        if isinstance(drives, int):
            list_drives = get_free_drives()[0:drives]
        elif isinstance(drives, str):
            list_drives = drives.split(' ')
        elif isinstance(drives, list):
            list_drives = drives

        string_drives = ' '.join([f'/dev/{drive}' for drive in list_drives])

        args = {
            '--name': name,
            '--level': level,
            '--drives': string_drives,
            '--sparepool': sparepool,
            '--synd_cnt': synd_cnt
        }
        return self._exec(self.eracli_command.add('create').add_dict(args))

    def destroy(self, name=None, _all=False):
        args = {'--name': name}
        return self._exec(self.eracli_command.add('destroy')
                                             .add_dict(args)
                                             .add_bool('--all', _all)
                                             .add_bool('--force', _all))

    def modify(
        self,
        name,
        init_prio=None,
        recon_prio=None,
        restripe_prio=None,
        sparepool=None,
    ):
        args = {
            '--name': name,
            '--init_prio': init_prio,
            '--recon_prio': recon_prio,
            '--restripe_prio': restripe_prio,
            '--sparepool': sparepool
        }
        return self._exec(self.eracli_command.add('modify').add_dict(args))

    def resize(self, name):
        args = {'--name': name}
        return self._exec(self.eracli_command.add('resize').add_dict(args))

    def restripe(
        self,
        name,
        level=None,
        drives=None,
        _start=False
    ):
        from framework.utils.drive_utils import get_free_drives
        if isinstance(drives, int):
            list_drives = get_free_drives()[0:drives]
        elif isinstance(drives, str):
            list_drives = drives.split(' ')

        string_drives = ' '.join([f'/dev/{drive}' for drive in list_drives])
        args = {'--name': name,
                '--level': level,
                '--drives': string_drives}

        return self._exec(self.eracli_command.add('restripe')
                                             .add_bool('start', _start)
                                             .add_dict(args))

    def show(
        self,
        extended=True,
        name=None,
        online=False,
        units=None
    ):
        """
        :result dict: {RAID_NAME: {RAID_NAME_params}, RAID_NAME2: {RAID_NAME2_params} }:
        """
        args = {
            '--format': 'json',
            '--name': name,
        }
        return self._exec(self.eracli_command.add('show').add_dict(args)
                                             .add_dict(args)
                                             .add_bool('--online', online)
                                             .add_bool('--extended', extended))
