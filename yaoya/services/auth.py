from asyncio import Protocol
from multiprocessing import AuthenticationError
from xml.dom import NotFoundErr

import dataset
from tinydb import Query
from yaoya.models.session import Session
from yaoya.models.user import User

from yaoya.services.mock import MockDB, MockSessionDB


class IAuthAPIClientService(Protocol):
    def login(self, user_id: str, password: str) -> str:
        pass

class MockAuthAPIClientService(IAuthAPIClientService):
    def __init__(self, mockdb: MockDB, session_db: MockSessionDB) -> None:
        self.mockdb = mockdb
        self.session_db = session_db

    # ログインに成功した場合、MockSessionDBにセッションを追加し、セッションIDを返す
    # ログインに失敗した場合、AuthenticationErrorを発生させる
    def login(self, user_id: str, password: str) -> str:
        if not self._verify_user(user_id, password):
            raise AuthenticationError

        session = Session(user_id=user_id)
        with self.session_db.connect() as db:
            db.insert(session.to_dict())

        return session.session_id

    # 指定されたユーザIDを持つユーザがMockDBのユーザテーブルに入ればTrueを返す
    # ※パスワードの検証は行わない
    def _verify_user(self, user_id: str, password: str) -> bool:
        with self.mockdb.connect() as db:
            table: dataset.Table = db["users"]
            user_data = table.find_one(user_id=user_id)

        return user_data is not None
    
class IUserAPIClientService(Protocol):
    def get_by_user_id(self, user_id: str) -> User:
        pass

    def get_by_session_id(self, session_id: str) -> User:
        pass

class MockUserAPIClientService(IUserAPIClientService):
    def __init__(self, mockdb: MockDB, session_db: MockSessionDB) -> None:
        self.mockdb = mockdb
        self.session_db = session_db

    def get_by_user_id(self, user_id: str) -> User:
        with self.mockdb.connect() as db:
            table: dataset.Table = db["users"]
            user_data = table.find_one(user_id=user_id)

        if user_data is None:
            raise NotFoundErr(user_id)

        return User.from_dict(user_data)

    def get_by_session_id(self, session_id: str) -> User:
        user_id = self._get_user_id(session_id)
        user = self.get_by_user_id(user_id)
        return user

    # セッションIDを用いてログインユーザのユーザIDを取得する
    def _get_user_id(self, session_id: str) -> str:
        with self.session_db.connect() as db:
            query = Query()
            doc = db.search(query.session_id == session_id)

        return doc[0]["user_id"]