"""Derive provider-facing JSON Schemas from canonical repo schemas (P2-01, NV-REQ-019).

Providers accept only JSON-Schema subsets (KB C1.3, C1.6, C1.9, C1.11). The repo schemas
stay the canonical gate; provider-side schemas are an optimization for constrained decoding.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Unsupported keywords per provider (KB C1.3, C1.6, C1.9, C1.11)
ANTHROPIC_UNSUPPORTED: Set[str] = {
    "minLength",
    "maxLength",
    "minimum",
    "maximum",
    "multipleOf",
    "$schema",
    "$id",
}

OPENAI_UNSUPPORTED: Set[str] = {
    "minLength",
    "maxLength",
    "pattern",
    "format",
    "minimum",
    "maximum",
    "multipleOf",
    "minItems",
    "maxItems",
    "if",
    "then",
    "else",
    "$schema",
    "$id",
}

GEMINI_UNSUPPORTED: Set[str] = {
    "minLength",
    "maxLength",
    "pattern",
    "if",
    "then",
    "else",
    "$defs",
    "$schema",
    "$id",
}

LOCAL_UNSUPPORTED: Set[str] = {
    "minLength",
    "maxLength",
    "pattern",
    "minimum",
    "maximum",
    "if",
    "then",
    "else",
    "$defs",
    "$schema",
    "$id",
}

UNSUPPORTED_KEYWORDS: Dict[str, Set[str]] = {
    "anthropic": ANTHROPIC_UNSUPPORTED,
    "openai": OPENAI_UNSUPPORTED,
    "gemini": GEMINI_UNSUPPORTED,
    "local": LOCAL_UNSUPPORTED,
    "fixture": set(),
}


def _clean_schema_node(node: Any, provider: str) -> Any:
    """Recursively strip unsupported keywords and enforce provider constraints."""
    if isinstance(node, list):
        return [_clean_schema_node(item, provider) for item in node]

    if not isinstance(node, dict):
        return node

    clean: Dict[str, Any] = {}
    unsupported = UNSUPPORTED_KEYWORDS.get(provider, set())

    # Filter and recurse
    for key, value in node.items():
        if key in unsupported:
            continue
        if key == "format" and provider == "gemini":
            # Gemini only supports date-time, date, time
            if value not in ("date-time", "date", "time"):
                continue
        clean[key] = _clean_schema_node(value, provider)

    # External $ref cannot be resolved over remote REST APIs (KB C1.6, C1.9)
    # Remove properties that reference external schemas (e.g. generation block stamped by pipeline)
    if "properties" in clean and isinstance(clean["properties"], dict):
        clean_props: Dict[str, Any] = {}
        for prop_name, prop_val in clean["properties"].items():
            if isinstance(prop_val, dict) and "$ref" in prop_val:
                ref_str = str(prop_val["$ref"])
                if ".json" in ref_str:
                    # External reference: pipeline stamps this, model must not generate it
                    continue
            clean_props[prop_name] = prop_val
        clean["properties"] = clean_props

        # If property was removed, also remove from required if present
        if "required" in clean and isinstance(clean["required"], list):
            clean["required"] = [r for r in clean["required"] if r in clean["properties"]]

    # Provider-specific object schema requirements
    is_object = clean.get("type") == "object" or "properties" in clean

    if provider == "openai":
        # Strict mode (KB C1.9): additionalProperties: false on every object
        if is_object:
            clean["additionalProperties"] = False
            if "properties" in clean and isinstance(clean["properties"], dict):
                clean["required"] = list(clean["properties"].keys())
    elif provider == "anthropic":
        # Anthropic structured output (KB C1.6): additionalProperties: false required
        if is_object:
            clean["additionalProperties"] = False

    return clean


def adapt_schema(schema: Dict[str, Any], provider: str) -> Dict[str, Any]:
    """Derive a provider-facing JSON schema from a repository schema.

    The original schema dictionary is never modified.
    """
    copied = copy.deepcopy(schema)
    return _clean_schema_node(copied, provider)


def get_provider_schema(contract: Dict[str, Any], provider: str,
                        root_dir: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """Return adapted schema if contract specifies structured_output: true, else None."""
    model_reqs = contract.get("model_requirements", {})
    if not model_reqs.get("structured_output", False):
        return None

    output_cfg = contract.get("output", {})
    schema_rel = output_cfg.get("schema")
    if not schema_rel:
        return None

    if root_dir is None:
        root_dir = Path(__file__).resolve().parent.parent

    schema_path = root_dir / schema_rel
    if not schema_path.is_file():
        raise FileNotFoundError(f"Contract schema not found: {schema_path}")

    raw_schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return adapt_schema(raw_schema, provider)
