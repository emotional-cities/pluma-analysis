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
    s3fs = S3FileSystem()

    def __init__(self,
                 root: str = '',
                 remotetype: RemoteType = RemoteType.WIN) -> None:

        self._remote = RemoteType.NONE
        self._root = root
        self.root = self._root

    # Instance properties
    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value: str):
        self._remote_type_conversion(value)
        value = self._format_os_path(value)
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

    def str(self):
        return self.root

    # Class methods
    def join_to_str(self, path: str) -> str:
        return self._format_os_path(os.path.join(self.root, path))

    def join(self, path: str):
        return ComplexPath(self.join_to_str(path))

    def append(self, path: str) -> None:
        self.root = self.join(path)

    def format(self, force_str: bool = False) -> str:
        if force_str is True:
            return self.root
        else:
            return self._dynamic_path_constructor(
                self.root
                )

    # Helper private methods
    def _format_os_path(self, path):
        if self.remote == RemoteType.WIN:
            return path.replace("/", "\\")
        elif self.remote == RemoteType.AWS:
            return path.replace("\\", "/")
        elif self.remote == RemoteType.UNIX:
            return path.replace("\\", "/")
        else:
            return path.replace("\\", "/")

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
            return self.s3fs.open(path)
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
    elif isinstance(root, ComplexPath):
        return root
    else:
        raise TypeError("Must be of str or ComplexPath type")


def ensure_strpath(root: Union[str, ComplexPath]) -> str:
    if isinstance(root, str):
        return root
    elif isinstance(root, ComplexPath):
        return ComplexPath(root)
    else:
        raise TypeError("Must be of str or ComplexPath type")