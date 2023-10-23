from __future__ import annotations
import json
from uuid import uuid4
from attr import dataclass
from yaoya.models.base import BaseDataModel


@dataclass(frozen=True)
class Session(BaseDataModel):
    user_id: str
    session_id: str = str(uuid4())

    def to_dict(self) -> dict[str, str]:
        return dict(
            session_id=self.session_id,
            user_id=self.user_id
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Session:
        return Session(
            session_id=data["session_id"],
            user_id=data["user_id"]
        )