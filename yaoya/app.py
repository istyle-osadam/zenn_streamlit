import streamlit as st
from yaoya.session import StreamlitSessionManager
from yaoya.pages.base import BasePage
from yaoya.const import SessionKey
from yaoya.exceptions import YaoyaError
class MultiPageApp:
    def __init__(self, ssm: StreamlitSessionManager, pages: list[BasePage], nav_label: str = "ページ一覧") -> None:
        self.pages = {page.page_id: page for page in pages}
        self.ssm = ssm
        self.nav_label = nav_label

    def render(self) -> None:
        # ページ選択ボックスを追加
        page_id = st.sidebar.selectbox(
            self.nav_label, # 選択ボックスのラベル
            list(self.pages.keys()), # ページ一覧
            format_func=lambda page_id: self.pages[page_id].title,
            key=SessionKey.PAGE_ID.name, # (B)
        )

        # ページ描画
        try:
            self.pages[page_id].render() # (A)
        except YaoyaError as e:
            st.error(e)