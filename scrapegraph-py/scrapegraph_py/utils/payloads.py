"""Helpers for normalizing SDK inputs into SGAI v2 API payloads."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from scrapegraph_py.models.shared import LlmConfig

DEFAULT_SCREENSHOT_FORMAT = {
    "type": "screenshot",
    "fullPage": False,
    "width": 1440,
    "height": 900,
    "quality": 80,
}


def schema_to_dict(schema: Optional[Any]) -> Optional[Dict[str, Any]]:
    """Convert a schema-like input into JSON Schema."""
    if schema is None:
        return None
    if isinstance(schema, dict):
        return schema
    if isinstance(schema, type) and issubclass(schema, BaseModel):
        return schema.model_json_schema()
    raise ValueError(
        "schema must be a dict (JSON Schema) or a Pydantic BaseModel class"
    )


def llm_config_to_dict(
    llm_config: Optional[LlmConfig | Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Normalize llmConfig payloads for json/summary scrape formats."""
    if llm_config is None:
        return None
    if isinstance(llm_config, LlmConfig):
        return llm_config.model_dump()
    if isinstance(llm_config, dict):
        return llm_config
    raise ValueError("llm_config must be a dict or LlmConfig instance")


def build_single_format_entry(format_name: str) -> Dict[str, Any]:
    """Build a default SGAI v2 format entry from a legacy single-format string."""
    normalized = format_name.strip().lower()

    if normalized == "markdown":
        return {"type": "markdown", "mode": "normal"}
    if normalized == "html":
        return {"type": "html", "mode": "normal"}
    if normalized == "screenshot":
        return dict(DEFAULT_SCREENSHOT_FORMAT)
    if normalized == "links":
        return {"type": "links"}
    if normalized == "images":
        return {"type": "images"}
    if normalized == "summary":
        return {"type": "summary"}
    if normalized == "branding":
        return {"type": "branding"}
    if normalized == "json":
        raise ValueError(
            "The 'json' format requires prompt/schema configuration. "
            "Use formats=[...] or the monitor prompt compatibility path."
        )

    raise ValueError(f"Unsupported format: {format_name}")


def build_json_format_entry(
    prompt: str,
    schema: Optional[Any] = None,
    llm_config: Optional[LlmConfig | Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build a json scrape format entry used by monitor compatibility shims."""
    entry: Dict[str, Any] = {
        "type": "json",
        "prompt": prompt,
        "mode": "normal",
    }
    schema_dict = schema_to_dict(schema)
    if schema_dict is not None:
        entry["schema"] = schema_dict
    llm_config_dict = llm_config_to_dict(llm_config)
    if llm_config_dict is not None:
        entry["llmConfig"] = llm_config_dict
    return entry


def normalize_format_entries(
    formats: Optional[List[Dict[str, Any]]] = None,
    legacy_format: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Normalize caller-provided formats into a SGAI-compliant formats array."""
    if formats:
        normalized_formats: List[Dict[str, Any]] = []
        for entry in formats:
            normalized_entry = dict(entry)
            if normalized_entry.get("type") == "json" and "schema" in normalized_entry:
                normalized_entry["schema"] = schema_to_dict(normalized_entry["schema"])
            if (
                normalized_entry.get("type") in {"json", "summary"}
                and "llmConfig" in normalized_entry
            ):
                normalized_entry["llmConfig"] = llm_config_to_dict(
                    normalized_entry["llmConfig"]
                )
            normalized_formats.append(normalized_entry)
        return normalized_formats

    return [build_single_format_entry(legacy_format or "markdown")]


def normalize_history_params(
    *,
    page: Optional[int] = None,
    limit: Optional[int] = None,
    service: Optional[str] = None,
    endpoint: Optional[str] = None,
    status: Optional[str] = None,
    offset: Optional[int] = None,
) -> Dict[str, Any]:
    """Map legacy history filters onto SGAI v2's page/limit/service contract."""
    if status is not None:
        raise ValueError("History status filtering is not supported by SGAI v2")

    if service and endpoint and service != endpoint:
        raise ValueError("service and endpoint cannot disagree")

    resolved_limit = limit
    resolved_page = page

    if offset is not None:
        offset_limit = limit or 20
        if offset % offset_limit != 0:
            raise ValueError("offset must be a multiple of limit to map onto page")
        inferred_page = (offset // offset_limit) + 1
        if page is not None and page != inferred_page:
            raise ValueError("page and offset point to different result windows")
        resolved_limit = offset_limit
        resolved_page = inferred_page

    params = {
        "page": resolved_page,
        "limit": resolved_limit,
        "service": service or endpoint,
    }
    return {key: value for key, value in params.items() if value is not None}
