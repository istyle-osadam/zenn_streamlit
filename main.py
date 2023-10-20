import streamlit as st

from yaoya.init_app import init_app, init_pages, init_session


if not st.session_state.get("is_started", False): # 初期化しているかの確認
    ssm = init_session() # session_stateの初期化
    pages = init_pages(ssm) # ページの初期化
    app = init_app(ssm, pages) # アプリケーションの初期化
    st.session_state["is_started"] = True
    st.session_state["app"] = app
    st.set_page_config(page_title="八百屋さんEC", layout="wide") # Streamlitのページ設定

app = st.session_state.get("app", None)
if app is not None:
    app.render()