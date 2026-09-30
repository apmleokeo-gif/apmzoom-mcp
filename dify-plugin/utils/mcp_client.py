"""Client for the public apMZoomAI MCP server (read-only, no authentication).

The server (https://www.apmzoom.com/mcp) is stateless: one JSON-RPC ``tools/call`` POST per tool call, no
session to open. It is the only network destination this plugin uses.
"""

from __future__ import annotations

import json
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any

import requests

USER_AGENT = "apmzoom-dify-plugin/0.0.1"
TIMEOUT = (5, 25)  # (connect, read) seconds

LANGS = ("en", "zh", "ko", "ja", "vi", "th", "id", "ms")
CATEGORIES = (
    "tee", "shirt", "knit", "cardigan", "hoodie", "sweater", "vest", "jacket", "coat", "trench", "padding",
    "suit", "jeans", "shorts", "jumpsuit", "dress", "skirt", "set", "top", "outer", "pants", "accessories",
    "shoes", "bags", "men",
)


class McpError(Exception):
    """The MCP server could not be reached or answered with something that is not a tool result."""


@dataclass
class McpToolResult:
    text: str
    data: dict[str, Any] | None
    is_error: bool


def _decode_body(response: requests.Response) -> dict[str, Any]:
    """The server answers plain JSON; an event-stream answer is also accepted (last ``data:`` line wins)."""
    if "text/event-stream" in response.headers.get("content-type", ""):
        last = ""
        for line in response.text.splitlines():
            if line.startswith("data:") and line[5:].strip():
                last = line[5:].strip()
        if not last:
            raise McpError("The apMZoomAI MCP server sent an empty event stream.")
        body = json.loads(last)
    else:
        body = response.json()
    if not isinstance(body, dict):
        raise McpError("The apMZoomAI MCP server sent an unexpected response.")
    return body


def call_tool(name: str, arguments: dict[str, Any]) -> McpToolResult:
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": arguments}}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": USER_AGENT,
    }
    try:
        response = requests.post("https://www.apmzoom.com/mcp", json=payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise McpError(f"Could not reach the apMZoomAI MCP server ({exc.__class__.__name__}).") from exc
    if response.status_code == 429:
        raise McpError("The apMZoomAI MCP server is limiting requests from this network address; try again in a minute.")
    if response.status_code >= 400:
        raise McpError(f"The apMZoomAI MCP server answered HTTP {response.status_code}.")
    try:
        body = _decode_body(response)
    except ValueError as exc:
        raise McpError("The apMZoomAI MCP server sent a response that is not valid JSON.") from exc
    error = body.get("error")
    if isinstance(error, dict):
        raise McpError(f"The apMZoomAI MCP server returned error {error.get('code')}: {error.get('message')}")
    result = body.get("result")
    if not isinstance(result, dict):
        raise McpError("The apMZoomAI MCP server sent a response without a result.")
    text = "\n".join(
        str(part.get("text", "")) for part in result.get("content") or [] if isinstance(part, dict) and part.get("type") == "text"
    ).strip()
    data = result.get("structuredContent")
    return McpToolResult(text=text, data=data if isinstance(data, dict) else None, is_error=bool(result.get("isError")))


def _text(value: Any, max_len: int) -> str | None:
    if value is None:
        return None
    cleaned = str(value).strip()[:max_len]
    return cleaned or None


def _int(value: Any, low: int, high: int) -> int | None:
    if value is None or value == "":
        return None
    try:
        number = int(float(value))
    except (TypeError, ValueError):
        return None
    return max(low, min(high, number))


def build_arguments(params: dict[str, Any], spec: dict[str, tuple[Any, ...]]) -> dict[str, Any]:
    """Keep only the documented arguments, trimmed and clamped to the ranges the server documents.

    ``spec`` maps an argument name to ("text", max_len), ("int", low, high) or ("choice", allowed_values).
    Empty and unknown values are dropped so the server applies its own defaults.
    """
    arguments: dict[str, Any] = {}
    for key, rule in spec.items():
        kind = rule[0]
        if kind == "text":
            value = _text(params.get(key), rule[1])
        elif kind == "int":
            value = _int(params.get(key), rule[1], rule[2])
        else:
            candidate = _text(params.get(key), 40)
            value = candidate if candidate in rule[1] else None
        if value is not None:
            arguments[key] = value
    return arguments


def emit(tool: Any, result: McpToolResult) -> Generator[Any, None, None]:
    """Yield the server's own text (what an agent reads) and its structured data (what a workflow reads)."""
    if result.text:
        yield tool.create_text_message(result.text)
    if result.data is not None:
        yield tool.create_json_message(result.data)
    elif result.is_error:
        yield tool.create_json_message({"error": result.text or "The apMZoomAI MCP server reported an error."})
