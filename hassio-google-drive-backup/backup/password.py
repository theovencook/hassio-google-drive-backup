import os
import yaml

from .logbase import LogBase
from .exceptions import SnapshotPasswordKeyInvalid
from .settings import Setting
from .config import Config


class Password(LogBase):
    def __init__(self, config: Config):
        self.config = config

    def resolve(self, password=None):
        if password is None:
            password = self.config.get(Setting.SNAPSHOT_PASSWORD)
        if len(password) == 0:
            return None
        if password.startswith("!secret "):
            if not os.path.isfile(self.config.get(Setting.SECRETS_FILE_PATH)):
                raise SnapshotPasswordKeyInvalid()
            with open(self.config.get(Setting.SECRETS_FILE_PATH)) as f:
                secrets_yaml = yaml.load(f, Loader=yaml.SafeLoader)
            key = password[len("!secret "):]
            if key not in secrets_yaml:
                raise SnapshotPasswordKeyInvalid()
            return str(secrets_yaml[key])
        else:
            return password
