#!/usr/bin/env python3
import argparse
import json

from _jira_common import build_api_url, build_headers, get_base_url, load_json, load_team_config, request_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update an existing Jira issue from a payload JSON file.")
    parser.add_argument("config_path", help="path to team-config JSON file")
    parser.add_argument("issue_key", help="Jira issue key, e.g. APP-123")
    parser.add_argument("payload_path", help="path to Jira update-issue payload JSON file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_team_config(args.config_path)
    payload = load_json(args.payload_path)
    headers = build_headers(config, include_content_type=True)
    base_url = get_base_url(config)
    response = request_json(
        method="PUT",
        url=build_api_url(base_url, f"rest/api/3/issue/{args.issue_key}"),
        headers=headers,
        payload=payload,
    )
    print(json.dumps({"ok": True, "response": response}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
