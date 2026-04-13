#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Tuple

from _jira_common import load_json, load_team_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a Jira create/update payload JSON file.")
    parser.add_argument("payload_path", help="path to the payload JSON file to validate")
    parser.add_argument("--config", help="optional path to team-config JSON for cross-checking projectKey")
    parser.add_argument("--field-mapping", help="optional path to field-mapping JSON for type/label checks")
    return parser.parse_args()


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def validate_description(
    description: Any,
    errors: List[str],
    warnings: List[str],
) -> None:
    """Validate the fields.description value.

    Accepts None/empty (error), plain string (warning — Jira Cloud prefers ADF),
    or an ADF document object.
    """
    if description in (None, "", []):
        errors.append("fields.description: missing or empty")
        return

    if isinstance(description, str):
        warnings.append("fields.description: plain text provided; Jira Cloud REST v3 expects ADF JSON")
        return

    if not isinstance(description, dict):
        errors.append("fields.description: must be a string or ADF object")
        return

    if description.get("type") != "doc":
        errors.append("fields.description.type: must be 'doc'")
    if description.get("version") != 1:
        errors.append("fields.description.version: must be 1")
    content = description.get("content")
    if not isinstance(content, list) or not content:
        warnings.append("fields.description.content: empty")


def validate_payload(
    payload: Any,
    config: Optional[Dict[str, Any]] = None,
    field_mapping: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Validate a Jira create/update payload dict.

    Returns ``{"ok": bool, "errors": [...], "warnings": [...]}``.
    Exits with ``ok: False`` as soon as a structural problem makes further
    validation meaningless (e.g. payload is not an object, or ``fields``
    is missing / not an object).
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(payload, dict):
        return {"ok": False, "errors": ["payload: must be a JSON object"], "warnings": warnings}

    if "intakeResult" in payload and "fields" not in payload:
        errors.append("payload: looks like an intake result, not a Jira create/update payload")
        return {"ok": False, "errors": errors, "warnings": warnings}

    fields = payload.get("fields")
    if not isinstance(fields, dict):
        errors.append("fields: must be an object")
        return {"ok": False, "errors": errors, "warnings": warnings}

    project = fields.get("project")
    if not isinstance(project, dict) or not is_non_empty_string(project.get("key")):
        errors.append("fields.project.key: missing or not a non-empty string")
    elif config and is_non_empty_string(config.get("projectKey")) and project.get("key") != config.get("projectKey"):
        errors.append(
            f"fields.project.key: '{project.get('key')}' does not match config.projectKey '{config.get('projectKey')}'"
        )

    if not is_non_empty_string(fields.get("summary")):
        errors.append("fields.summary: missing or empty")

    issuetype = fields.get("issuetype")
    if not isinstance(issuetype, dict) or not any(is_non_empty_string(issuetype.get(k)) for k in ("name", "id")):
        errors.append("fields.issuetype: must be an object with a non-empty 'name' or 'id'")

    validate_description(fields.get("description"), errors, warnings)

    labels = fields.get("labels")
    if labels is not None and (
        not isinstance(labels, list) or any(not is_non_empty_string(label) for label in labels)
    ):
        errors.append("fields.labels: must be a list of non-empty strings")

    components = fields.get("components")
    if components is not None and not isinstance(components, list):
        errors.append("fields.components: must be a list")

    priority = fields.get("priority")
    if priority is not None and (
        not isinstance(priority, dict) or not any(is_non_empty_string(priority.get(k)) for k in ("name", "id"))
    ):
        errors.append("fields.priority: must be an object with a non-empty 'name' or 'id'")

    assignee = fields.get("assignee")
    if assignee is not None:
        if not isinstance(assignee, dict):
            errors.append("fields.assignee: must be an object")
        elif not any(is_non_empty_string(assignee.get(k)) for k in ("accountId", "id", "name")):
            warnings.append("fields.assignee: no accountId/id/name found; Jira Cloud requires accountId")

    if field_mapping:
        type_map = field_mapping.get("typeMap")
        if type_map is not None and not isinstance(type_map, dict):
            errors.append("field-mapping.typeMap: must be an object")
        platform_label_map = field_mapping.get("platformLabelMap")
        if platform_label_map is not None and not isinstance(platform_label_map, dict):
            errors.append("field-mapping.platformLabelMap: must be an object")

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main() -> None:
    args = parse_args()
    payload = load_json(args.payload_path)
    config = load_team_config(args.config) if args.config else None
    field_mapping = load_json(args.field_mapping) if args.field_mapping else None

    result = validate_payload(payload, config=config, field_mapping=field_mapping)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
