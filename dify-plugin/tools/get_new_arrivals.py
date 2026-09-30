from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.mcp_client import CATEGORIES, LANGS, build_arguments, call_tool, emit

ARGUMENTS = {
    "hours": ("int", 1, 168),
    "building": ("text", 40),
    "category": ("choice", CATEGORIES),
    "lang": ("choice", LANGS),
    "limit": ("int", 1, 30),
}


class GetNewArrivalsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        arguments = build_arguments(tool_parameters, ARGUMENTS)
        yield from emit(self, call_tool("get_new_arrivals", arguments))
