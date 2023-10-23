from enum import Enum, auto

class PageId(Enum):
    PUBLIC_LOGIN = auto() 

class SessionKey(Enum):
    AUTH_API_CLIENT = auto() 
    USER_API_CLIENT = auto() 
    SESSION_ID = auto() 
    USERBOX = auto() 
    USER = auto()
    PAGE_ID = auto()


class UserRole(Enum):
    ADMIN = auto()
    MEMBER = auto()