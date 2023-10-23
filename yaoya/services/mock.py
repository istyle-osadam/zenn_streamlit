
from datetime import date
import dataset
from contextlib import contextmanager
from typing import Generator
from pathlib import Path
from tinydb import TinyDB
from yaoya.const import UserRole

from yaoya.models.user import User

class MockDB:
    def __init__(self, dbpath: Path) -> None:
        s_dbpath = str(dbpath)
        self._dbname = f"sqlite:///{s_dbpath}"
        #self._init_mock_db() # 今後の章で実装

    @contextmanager
    def connect(self) -> Generator[dataset.Database, None, None]:
        db = dataset.connect(self._dbname)
        db.begin()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
     
    def _init_mock_db(self) -> None:
        self._create_mock_user_table()

    def _create_mock_user_table(self) -> None:
        mock_users = [
            User(
                user_id="member",
                name="会員",
                birthday=date(2000, 1, 1),
                email="guest@example.com",
                role=UserRole.MEMBER,
            ),
            User(
                user_id="admin",
                name="管理者",
                birthday=date(2000, 1, 1),
                email="admin@example.com",
                role=UserRole.ADMIN,
            ),
        ]
        with self.connect() as db:
            table: dataset.Table = db["users"]
            for mock_user in mock_users:
                table.insert(mock_user.to_dict())   
    #def _init_mock_db(self) -> None:
    #    self._create_mock_user_table()
    #    self._create_mock_item_table()

dbpath = Path("sample.db")
mock_db = MockDB(dbpath)

class MockSessionDB:
    def __init__(self, dbpath: Path) -> None:
        self._db = TinyDB(dbpath)

    @contextmanager
    def connect(self) -> Generator[TinyDB, None, None]:
        try:
            yield self._db
        except Exception as e:
            raise e

dbpath = Path("sample.json")
mock_session_db = MockSessionDB(dbpath)


# With句でテーブルの定義&データの追加
with mock_db.connect() as db:
    table: dataset.Table = db["samples"]
    print(table.find_one(id="001"))