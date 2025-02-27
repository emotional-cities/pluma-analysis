import os
import glob

from enum import Enum
from typing import Union, List


class RemoteType(Enum):
    NONE = ""
    AWS = "AWS"
    WIN = "WIN"
    UNIX = "UNIX"


class ComplexPath:
    s3fs = None  # Stores the s3fs object that is instantiated when needed

    def __init__(self, path: str = "") -> None:
        self._remote = RemoteType.NONE
        self._path = path
        self.path = self._path

    def open(self, *args, **kwargs):
        if self.iss3f():
            return self.s3fs.open(self.path, *args, **kwargs)
        else:
            return open(self.path, *args, **kwargs)

    def exists_s3fs(self):
        return self.s3fs is not None

    # Instance properties
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: str):
        self._remote_type_conversion(value)
        value = self._format_os_path(value)
        self._path = value

    @property
    def remote(self):
        return self._remote

    def iswin(self):
        return self.remote == RemoteType.WIN

    def iss3f(self):
        return self.remote == RemoteType.AWS

    def join(self, value: Union[str, list]):
        if isinstance(value, str):
            self.path = os.path.join(self.path, value)
        elif isinstance(value, list):
            _path = self.path
            for ss in value:
                _path = os.path.join(_path, ss)
            self.path = _path
        else:
            raise ValueError("")

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
        self._remote = self._parse_remote_type(new_root)
        if (self._remote == RemoteType.AWS) and (self.s3fs is None):
            from s3fs.core import S3FileSystem

            self.s3fs = S3FileSystem()

    @staticmethod
    def _parse_remote_type(new_root: str) -> RemoteType:
        if r"s3://" in new_root:
            return RemoteType.AWS
        else:
            return RemoteType.WIN

    def __str__(self) -> str:
        return f"@({self.remote.value}) --> {self.path}"

    def __repr__(self) -> str:
        return f"@({self.remote.value}) --> {self.path}"

    def glob(self, path: str = None) -> List:
        if path is None:
            path = self.path
        if self.iss3f() is True:
            _list = self.s3fs.glob(path)
            _list = [(r"s3://" + p) for p in _list]
            return _list
        else:
            return glob.glob(path)

    def isfile(self, path: str = None) -> bool:
        if path is None:
            path = self.path
        if self.iss3f() is True:
            return self.s3fs.isfile(path)
        else:
            return os.path.isfile(path)

    def isdir(self, path: str = None) -> bool:
        if path is None:
            path = self.path
        if self.iss3f() is True:
            return self.s3fs.isdir(path)
        else:
            return os.path.isdir(path)


# ----- Helper functions -----


def ensure_complexpath(in_path: Union[str, ComplexPath]) -> ComplexPath:
    if isinstance(in_path, str):
        return ComplexPath(path=in_path)
    elif isinstance(in_path, ComplexPath):
        return ComplexPath(in_path.path)
    else:
        raise TypeError(f"Must be of str or ComplexPath type. Got {type(in_path)}")
