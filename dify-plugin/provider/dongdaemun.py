from typing import Any

from dify_plugin import ToolProvider


class DongdaemunProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # The apMZoomAI public MCP server is read-only and needs no credentials.
        pass
