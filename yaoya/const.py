from enum import Enum, auto

class PageId(Enum):
    PAGE_ID = auto()

class SessionKey(Enum):
    USER = auto()
    PAGE_ID = auto()


class UserRole(Enum):
    ADMIN = auto()
    MEMBER = auto()