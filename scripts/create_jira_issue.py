#!/usr/bin/env python3
import argparse
import json

from _jira_common import (
    build_api_url,
    build_headers,
    get_base_url,
    load_json,
    load_team_config,
    request_json,
    summarize_jira_response,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="用 payload JSON 檔建立 Jira 議題。")
    parser.add_argument("config_path", help="team-config JSON 檔路徑")
    parser.add_argument("payload_path", help="Jira 建立議題 payload JSON 檔路徑")
    parser.add_argument("--verbose", action="store_true", help="包含完整 Jira 回應")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_team_config(args.config_path)
    payload = load_json(args.payload_path)
    headers = build_headers(config, include_content_type=True)
    base_url = get_base_url(config)
    response = request_json(
        method="POST",
        url=build_api_url(base_url, "rest/api/3/issue"),
        headers=headers,
        payload=payload,
    )
    result = summarize_jira_response(response, base_url=base_url, verbose=args.verbose)
    result["action"] = "create"
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
