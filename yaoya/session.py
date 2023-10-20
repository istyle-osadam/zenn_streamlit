import streamlit as st
from yaoya.models.user import User

class StreamlitSessionManager:
    def __init__(self) -> None:
        self._session_state = st.session_state

    def get_user(self) -> User:
        return self._session_state["user"]

    def set_user(self, user: User) -> None:
        self._session_state["user"] = user