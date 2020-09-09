from datetime import datetime
import os
import subprocess

from . import db


class BackUp(object):
    def __init__(self, backup_id=None):
        self.backup_id = backup_id or datetime.now().strftime('%Y%m%d.%H.%M.%S')
        self.db_prefix = 'db.'
        self.backup_path = self.db_prefix + self.backup_id

    @property
    def exists(self):
        return os.path.exists(self.backup_path)


def backup_db(backup_id=None):
    bk_up = BackUp(backup_id)
    cmd = ['cp', db.sqlite_db['database'], bk_up.backup_path]
    print(cmd)
    subprocess.call(cmd)
    return bk_up.backup_id


def restore_db(backup_id):
    bk_up = BackUp(backup_id)
    if bk_up.exists:
        new_bk_id = backup_db()
        restore_cmd = ['cp', bk_up.backup_path, db.sqlite_db['database']]
        print(restore_cmd)
        response = f'New backup {new_bk_id} created. Backup {backup_id} restored.'
    else:
        response = f'Backup {backup_id} does not exist'
    return response


