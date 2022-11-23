import os

from enum import Enum
from typing import Union

from s3fs.core import S3FileSystem


class RemoteType (Enum):
    NONE = ''
    AWS = 'AWS'
    WIN = 'WIN'
    UNIX = 'UNIX'


class ComplexPath():
    def __init__(self,
                 root: str = '',
                 remotetype: RemoteType = RemoteType.WIN) -> None:

        self._s3fs = S3FileSystem()
        self._remote = RemoteType.NONE
        self._root = self.root = root

    # Instance properties
    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value: str):
        self._remote_type_conversion(value)
        self._root = value

    @property
    def remote(self):
        return self._remote

    @remote.setter
    def remote(self, value: RemoteType):
        self._remote = value

    def iswin(self):
        return self.remote == RemoteType.WIN

    def iss3f(self):
        return self.remote == RemoteType.AWS

    # Class methods
    def join(self, path: str, force_str: bool = False) -> str:
        if force_str is True:
            return os.path.join(self.root, path)
        else:
            return self._dynamic_path_constructor(
                os.path.join(self.root, path)
                )

    def format(self, force_str: bool = False) -> str:
        if force_str is True:
            return self.root
        else:
            return self._dynamic_path_constructor(
                self.root
                )

    # Helper private methods
    def _remote_type_conversion(self, new_root: str):
        self.remote = self._parse_remote_type(new_root)

    @staticmethod
    def _parse_remote_type(new_root: str) -> RemoteType:
        if r's3://' in new_root:
            return RemoteType.AWS
        else:
            return RemoteType.WIN

    def _dynamic_path_constructor(self, path: str):
        if self._remote == RemoteType.WIN:
            return path
        elif self._remote == RemoteType.AWS:
            return self._s3fs.open(path)
        else:
            return path

    def __str__(self) -> str:
        return f'@({self.remote.value}) --> {self.root}'

    def __repr__(self) -> str:
        return f'@({self.remote.value}) --> {self.root}'

# ----- Helper functions -----


def ensure_complexpath(root: Union[str, ComplexPath]) -> ComplexPath:
    if isinstance(root, str):
        return ComplexPath(root=root)
    else:
        return root