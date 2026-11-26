"""Parameters declared on an OpenAPI path item (shared by its operations, e.g.
`ruleId` on `/v1/ads/rules/{ruleId}`) must reach the generated SDK methods and
MCP tools. They were dropped, so `ad_rules_get_ad_rule` took no rule id and
requested `/v1/ads/rules/{ruleId}` literally."""

from __future__ import annotations

import importlib
import re
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import httpx
import pytest
import respx
import yaml
from fastmcp import Client

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
SPEC_PATH = Path(__file__).resolve().parents[1] / "openapi.yaml"

SPEC: dict[str, Any] = {
    "components": {
        "parameters": {
            "PortalToken": {
                "name": "token",
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
            }
        }
    }
}
RULE_ID = {
    "name": "ruleId",
    "in": "path",
    "required": True,
    "schema": {"type": "string"},
}


@pytest.fixture
def generators(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend(str(SCRIPTS))
    return (
        importlib.import_module("generate_resources"),
        importlib.import_module("generate_mcp_tools"),
        importlib.import_module("openapi_body"),
    )


def _sdk_resource(generator, path: str, method: str, path_item: dict, operation: dict):
    source = generator.generate_resource_class(
        "probe",
        [
            {
                "operation_id": "probeOp",
                "http_method": method,
                "path": path,
                "summary": "Probe",
                "description": "",
                "params": generator.extract_parameters(operation, SPEC, path_item),
            }
        ],
    )
    namespace: dict[str, Any] = {}
    exec(compile(source, "<generated-probe>", "exec"), namespace)
    client = Mock()
    return namespace["ProbeResource"](client), client


def test_sdk_method_takes_a_plain_path_item_parameter(generators) -> None:
    resources, _, _ = generators
    resource, client = _sdk_resource(
        resources, "/v1/ads/rules/{ruleId}", "delete", {"parameters": [RULE_ID]}, {}
    )

    resource.probe_op(rule_id="rule_1")

    client._delete.assert_called_once_with("/v1/ads/rules/rule_1")


def test_sdk_method_takes_a_referenced_path_item_parameter(generators) -> None:
    resources, _, _ = generators
    path_item = {
        "parameters": [
            {"$ref": "#/components/parameters/PortalToken"},
            {
                "name": "accountId",
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
            },
        ]
    }
    resource, client = _sdk_resource(
        resources,
        "/public/portal/{token}/accounts/{accountId}",
        "delete",
        path_item,
        {},
    )

    resource.probe_op(token="tok_1", account_id="acc_1")

    client._delete.assert_called_once_with("/public/portal/tok_1/accounts/acc_1")


def test_operation_parameter_overrides_the_path_item_one(generators) -> None:
    _, _, openapi_body = generators
    path_item = {
        "parameters": [
            RULE_ID,
            {"name": "view", "in": "query", "schema": {"type": "string"}},
        ]
    }
    operation = {
        "parameters": [
            {
                "name": "ruleId",
                "in": "path",
                "required": True,
                "description": "Op-level",
            },
            {
                "name": "ruleId",
                "in": "query",
                "description": "Same name, other location",
            },
        ]
    }

    merged = openapi_body.merge_parameters(path_item, operation, SPEC)

    assert [(p["name"], p["in"], p.get("description")) for p in merged] == [
        ("view", "query", None),
        ("ruleId", "path", "Op-level"),
        ("ruleId", "query", "Same name, other location"),
    ]


def test_mcp_tool_takes_path_item_parameters(generators) -> None:
    _, mcp_tools, _ = generators
    path_item = {
        "parameters": [{"$ref": "#/components/parameters/PortalToken"}, RULE_ID]
    }
    operation = {
        "parameters": [{"name": "limit", "in": "query", "schema": {"type": "integer"}}]
    }

    params = mcp_tools.extract_parameters(operation, SPEC, path_item)

    assert [(p["name"], p["required"]) for p in params] == [
        ("token", True),
        ("rule_id", True),
        ("limit", False),
    ]


def test_every_path_placeholder_in_the_spec_is_a_generated_parameter(
    generators,
) -> None:
    resources, mcp_tools, _ = generators
    spec = yaml.safe_load(SPEC_PATH.read_text())
    missing = []
    for path, path_item in spec["paths"].items():
        placeholders = set(re.findall(r"{([^}]+)}", path))
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue
            sdk_params = resources.extract_parameters(operation, spec, path_item)
            sdk_path = {p["original_name"] for p in sdk_params if p["in"] == "path"}
            mcp_names = {
                p["name"]
                for p in mcp_tools.extract_parameters(operation, spec, path_item)
            }
            wanted_mcp = {mcp_tools.camel_to_snake(n) for n in placeholders}
            if placeholders - sdk_path or wanted_mcp - mcp_names:
                missing.append(f"{method.upper()} {path}")

    assert missing == []


@pytest.fixture
def api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZERNIO_API_KEY", "test_api_key")
    monkeypatch.setenv("ZERNIO_BASE_URL", "https://api.test.com")


@pytest.mark.parametrize(
    ("tool", "arguments", "method", "path"),
    [
        ("ad_rules_get_ad_rule", {"rule_id": "rule_1"}, "GET", "/v1/ads/rules/rule_1"),
        (
            "ad_rules_delete_ad_rule",
            {"rule_id": "rule_1"},
            "DELETE",
            "/v1/ads/rules/rule_1",
        ),
        (
            "ad_rules_update_ad_rule",
            {"rule_id": "rule_1", "name": "Pause losers"},
            "PATCH",
            "/v1/ads/rules/rule_1",
        ),
        (
            "automations_get_automation",
            {"automation_id": "auto_1"},
            "GET",
            "/v1/automations/auto_1",
        ),
        (
            "automations_delete_automation",
            {"automation_id": "auto_1"},
            "DELETE",
            "/v1/automations/auto_1",
        ),
        (
            "conversions_get_tracking_site",
            {"site_id": "site_1"},
            "GET",
            "/v1/tracking-sites/site_1",
        ),
        (
            "creator_campaigns_list_campaign_payout_batches",
            {"campaign_id": "camp_1"},
            "GET",
            "/v1/creator-campaigns/camp_1/payout-batches",
        ),
        (
            "creator_portal_remove_creator_account",
            {"token": "tok_1234567890abcdef", "account_id": "acc_1"},
            "DELETE",
            "/public/creator-campaigns/tok_1234567890abcdef/accounts/acc_1",
        ),
    ],
)
@pytest.mark.usefixtures("api_env")
@respx.mock
async def test_mcp_tool_requests_the_filled_in_url(
    tool: str, arguments: dict[str, Any], method: str, path: str
) -> None:
    from late.mcp.server import mcp

    route = respx.route(url__startswith="https://api.test.com/").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    async with Client(mcp) as client:
        result = await client.call_tool(
            "call_tool", {"name": tool, "arguments": arguments}, raise_on_error=False
        )

    assert not result.is_error, result.content[0].text
    request = route.calls.last.request
    assert (request.method, request.url.path) == (method, path)
