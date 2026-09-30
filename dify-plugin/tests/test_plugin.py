"""Offline tests for the apMZoomAI Dongdaemun Dify plugin (run from the plugin root: pytest tests)."""

import json
import os
import sys

import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from utils import mcp_client  # noqa: E402
from utils.mcp_client import LANGS, McpError, build_arguments, call_tool, emit  # noqa: E402


class FakeResponse:
    def __init__(self, body, status=200, content_type="application/json"):
        self._body = body
        self.status_code = status
        self.headers = {"content-type": content_type}
        self.text = body if isinstance(body, str) else json.dumps(body)

    def json(self):
        if isinstance(self._body, str):
            return json.loads(self._body)
        return self._body


class FakeTool:
    def create_text_message(self, text):
        return ("text", text)

    def create_json_message(self, data):
        return ("json", data)


def ok_body(text="hello", data=None, is_error=False):
    result = {"content": [{"type": "text", "text": text}]}
    if data is not None:
        result["structuredContent"] = data
    if is_error:
        result["isError"] = True
    return {"jsonrpc": "2.0", "id": 1, "result": result}


def test_build_arguments_trims_clamps_and_drops_unknown():
    spec = {"query": ("text", 10), "lang": ("choice", LANGS), "limit": ("int", 1, 20), "building": ("text", 40)}
    params = {"query": "  linen dress for summer  ", "lang": "xx", "limit": 99, "building": "", "extra": "ignored"}
    assert build_arguments(params, spec) == {"query": "linen dres", "limit": 20}
    assert build_arguments({"limit": "0", "lang": "ko"}, spec) == {"lang": "ko", "limit": 1}
    assert build_arguments({"limit": "abc"}, spec) == {}


def test_call_tool_posts_json_rpc_and_reads_result(monkeypatch):
    seen = {}

    def fake_post(url, json=None, headers=None, timeout=None):  # noqa: A002
        seen.update(url=url, payload=json, headers=headers, timeout=timeout)
        return FakeResponse(ok_body("3 items", {"count": 3}))

    monkeypatch.setattr(mcp_client.requests, "post", fake_post)
    result = call_tool("search_products", {"query": "knit"})
    assert seen["url"] == "https://www.apmzoom.com/mcp"
    assert seen["payload"]["method"] == "tools/call"
    assert seen["payload"]["params"] == {"name": "search_products", "arguments": {"query": "knit"}}
    assert "Authorization" not in seen["headers"]
    assert (result.text, result.data, result.is_error) == ("3 items", {"count": 3}, False)


def test_tool_level_error_is_returned_as_text_not_raised(monkeypatch):
    monkeypatch.setattr(
        mcp_client.requests, "post", lambda *a, **k: FakeResponse(ok_body("Item is not listed", is_error=True))
    )
    result = call_tool("get_product", {"id": "x"})
    assert result.is_error
    messages = list(emit(FakeTool(), result))
    assert messages == [("text", "Item is not listed"), ("json", {"error": "Item is not listed"})]


def test_emit_yields_text_then_structured_data():
    result = mcp_client.McpToolResult(text="t", data={"a": 1}, is_error=False)
    assert list(emit(FakeTool(), result)) == [("text", "t"), ("json", {"a": 1})]


def test_event_stream_response_is_accepted(monkeypatch):
    sse = "event: message\ndata: " + json.dumps(ok_body("via sse", {"n": 1})) + "\n\n"
    monkeypatch.setattr(
        mcp_client.requests, "post", lambda *a, **k: FakeResponse(sse, content_type="text/event-stream")
    )
    assert call_tool("list_buildings", {}).text == "via sse"


@pytest.mark.parametrize(
    "response, fragment",
    [
        (FakeResponse({}, status=429), "limiting requests"),
        (FakeResponse({}, status=503), "HTTP 503"),
        (FakeResponse({"jsonrpc": "2.0", "id": 1, "error": {"code": -32601, "message": "nope"}}), "-32601"),
        (FakeResponse({"jsonrpc": "2.0", "id": 1}), "without a result"),
        (FakeResponse("not json"), "not valid JSON"),
    ],
)
def test_transport_problems_raise_mcp_error(monkeypatch, response, fragment):
    monkeypatch.setattr(mcp_client.requests, "post", lambda *a, **k: response)
    with pytest.raises(McpError) as info:
        call_tool("search_products", {"query": "x"})
    assert fragment in str(info.value)


def test_network_failure_raises_mcp_error_without_leaking_details(monkeypatch):
    def boom(*a, **k):
        raise mcp_client.requests.ConnectTimeout("secret-host-detail")

    monkeypatch.setattr(mcp_client.requests, "post", boom)
    with pytest.raises(McpError) as info:
        call_tool("search_products", {"query": "x"})
    assert "ConnectTimeout" in str(info.value) and "secret-host-detail" not in str(info.value)


def test_every_tool_yaml_matches_its_python_source_and_the_manifest():
    manifest = yaml.safe_load(open(os.path.join(ROOT, "manifest.yaml"), encoding="utf-8"))
    provider = yaml.safe_load(open(os.path.join(ROOT, manifest["plugins"]["tools"][0]), encoding="utf-8"))
    assert len(provider["tools"]) == 5
    for rel in provider["tools"]:
        tool = yaml.safe_load(open(os.path.join(ROOT, rel), encoding="utf-8"))
        source = tool["extra"]["python"]["source"]
        assert os.path.isfile(os.path.join(ROOT, source)), source
        assert source == f"tools/{tool['identity']['name']}.py"
        for param in tool["parameters"]:
            assert param["form"] == "llm"
            if param["type"] == "select":
                assert param["options"], param["name"]


@pytest.mark.skipif(not os.environ.get("APMZOOM_LIVE"), reason="set APMZOOM_LIVE=1 to call the real server")
def test_live_server_round_trip():
    buildings = call_tool("list_buildings", {"lang": "en"})
    assert not buildings.is_error and buildings.data and buildings.data.get("buildings")
    search = call_tool("search_products", {"query": "dress", "limit": 2})
    assert not search.is_error and search.data and search.data["count"] >= 1
    item_id = search.data["products"][0]["id"]
    detail = call_tool("get_product", {"id": item_id})
    assert not detail.is_error and item_id in json.dumps(detail.data)
    assert call_tool("get_new_arrivals", {"hours": 168, "limit": 3}).text
    assert call_tool("find_stalls", {"query": "FRANC"}).text
    missing = call_tool("get_product", {"id": "00000000-0000-0000-0000-000000000000"})
    assert missing.is_error and "not listed" in missing.text
