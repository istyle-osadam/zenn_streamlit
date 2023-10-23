import streamlit as st
from yaoya.const import SessionKey
from yaoya.models.user import User
from yaoya.services.auth import IAuthAPIClientService, IUserAPIClientService

class StreamlitSessionManager:
    def __init__(self,
        auth_api_client: IAuthAPIClientService,
        user_api_client: IUserAPIClientService) -> None:
        self._session_state = st.session_state
        self._session_state[SessionKey.AUTH_API_CLIENT.name] = auth_api_client
        self._session_state[SessionKey.USER_API_CLIENT.name] = user_api_client
        
    def get_user(self) -> User:
        return self._session_state["user"]

    def set_user(self, user: User) -> None:
        self._session_state["user"] = user