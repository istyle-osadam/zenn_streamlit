from pathlib import Path
from tempfile import TemporaryDirectory
from yaoya.app import MultiPageApp
from yaoya.const import PageId
from yaoya.pages.base import BasePage
from yaoya.pages.public.login import LoginPage
from yaoya.services.auth import MockAuthAPIClientService, MockUserAPIClientService
from yaoya.services.mock import MockDB, MockSessionDB
from yaoya.session import StreamlitSessionManager


    
def init_session() -> StreamlitSessionManager:
    mockdir = Path(TemporaryDirectory().name) # (A)
    mockdir.mkdir(exist_ok=True)
    mockdb = MockDB(mockdir.joinpath("mock.db"))
    session_db = MockSessionDB(mockdir.joinpath("session.json"))
    ssm = StreamlitSessionManager(
        auth_api_client=MockAuthAPIClientService(mockdb, session_db), 
        user_api_client=MockUserAPIClientService(mockdb, session_db)
    )
    return ssm

# ページの初期化
def init_pages(ssm: StreamlitSessionManager) -> list[BasePage]:
    pages = [
        LoginPage(page_id=PageId.PUBLIC_LOGIN.name, title="ログイン", ssm=ssm)
    ]
    return pages

# アプリケーションの初期化
def init_app(ssm: StreamlitSessionManager, pages: list[BasePage]) -> MultiPageApp:
    app = MultiPageApp(ssm, pages)
    return app