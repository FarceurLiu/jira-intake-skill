#!/usr/bin/env python3
import argparse
import json

from _jira_common import build_api_url, build_headers, get_base_url, load_team_config, request_json, resolve_transition_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Move a Jira issue to a new status via a workflow transition.")
    parser.add_argument("config_path", help="path to team-config JSON file")
    parser.add_argument("issue_key", help="Jira issue key, e.g. APP-123")
    parser.add_argument(
        "transition_ref",
        help="transition id, logical key from statusTransitionMap in config, or status name",
    )
    parser.add_argument("--dry-run", action="store_true", help="resolve transition id but do not call Jira")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_team_config(args.config_path)
    transition_id = resolve_transition_id(
        config=config,
        issue_key=args.issue_key,
        transition_ref=args.transition_ref,
    )

    result = {
        "ok": True,
        "issue": args.issue_key,
        "transitionRef": args.transition_ref,
        "transitionId": transition_id,
        "dryRun": args.dry_run,
    }

    if not args.dry_run:
        headers = build_headers(config, include_content_type=True)
        base_url = get_base_url(config)
        response = request_json(
            method="POST",
            url=build_api_url(base_url, f"rest/api/3/issue/{args.issue_key}/transitions"),
            headers=headers,
            payload={"transition": {"id": transition_id}},
        )
        result["response"] = response

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
