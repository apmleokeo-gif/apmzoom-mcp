from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.mcp_client import LANGS, build_arguments, call_tool, emit

ARGUMENTS = {
        "id": ("text", 64),
        "lang": ("choice", LANGS),
    }


class GetProductTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        arguments = build_arguments(tool_parameters, ARGUMENTS)
        yield from emit(self, call_tool("get_product", arguments))
