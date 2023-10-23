from yaoya.session import StreamlitSessionManager
from yaoya.const import PageId

class BasePage:
    def __init__(self, page_id: PageId, title: str, ssm: StreamlitSessionManager) -> None:
        self.page_id = page_id.name
        self.title = title
        self.ssm = ssm

    def render(self) -> None:
        pass