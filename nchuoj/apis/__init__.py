from . import user
from . import course

from .user import *
from .course import *


__all__ = [
    *user.__all__,
    *course.__all__
]