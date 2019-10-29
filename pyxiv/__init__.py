"""
Pixiv API library
"""
__version__ = '4.2'

from .aapi import AppPixivAPI
from .papi import PixivAPI
from .utils import PixivError

__all__ = ("PixivAPI", "AppPixivAPI", "PixivError")
