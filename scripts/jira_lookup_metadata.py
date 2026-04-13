#!/usr/bin/env python3
import argparse
import json
from urllib import parse

from _jira_common import build_api_url, build_headers, fail, fetch_all_pages, get_base_url, load_team_config, request_json

MODES = (
    "fields",
    "transitions",
    "issue-types",
    "projects",
    "boards",
    "sprints",
    "members",
)

# Modes that auto-paginate via fetch_all_pages.
# All others call request_json once and return the raw response.
PAGINATED_MODES = {"projects", "boards", "sprints", "members"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Look up Jira metadata.\n\n"
            "modes:\n"
            "  fields       list all custom and system fields\n"
            "  transitions  list transitions for an issue  (ref = issue key)\n"
            "  issue-types  list issue types for projectKey in config\n"
            "  projects     list accessible projects  [paginated]\n"
            "  boards       list boards for projectKey in config  [paginated]\n"
            "  sprints      list active/future sprints  (ref = boardId, or defaultBoardId in config)  [paginated]\n"
            "  members      list assignable members for projectKey in config  [paginated]\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("config_path", help="path to team-config JSON file")
    parser.add_argument("mode", choices=MODES)
    parser.add_argument(
        "ref",
        nargs="?",
        help="issue key (for transitions) or board id (for sprints)",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=50,
        metavar="N",
        help="items fetched per request for paginated modes (default: 50)",
    )
    return parser.parse_args()


def _project_key(config: dict) -> str:
    key = str(config.get("projectKey", "")).strip()
    if not key:
        fail("missing projectKey in config")
    return key


def main() -> None:
    args = parse_args()
    config = load_team_config(args.config_path)
    base_url = get_base_url(config)
    headers = build_headers(config)

    # ── non-paginated modes ───────────────────────────────────────────────────

    if args.mode == "fields":
        data = request_json(method="GET", url=build_api_url(base_url, "rest/api/3/field"), headers=headers)
        print(json.dumps({"ok": True, "mode": args.mode, "data": data}, ensure_ascii=False, indent=2))
        return

    if args.mode == "issue-types":
        query = parse.urlencode({"projectKeys": _project_key(config)})
        url = f"{build_api_url(base_url, 'rest/api/3/issue/createmeta')}?{query}"
        data = request_json(method="GET", url=url, headers=headers)
        print(json.dumps({"ok": True, "mode": args.mode, "data": data}, ensure_ascii=False, indent=2))
        return

    if args.mode == "transitions":
        if not args.ref:
            fail(
                "transitions mode requires an issue key",
                details={"usage": "jira_lookup_metadata.py <config> transitions <issue-key>"},
            )
        data = request_json(
            method="GET",
            url=build_api_url(base_url, f"rest/api/3/issue/{args.ref}/transitions"),
            headers=headers,
        )
        print(json.dumps({"ok": True, "mode": args.mode, "data": data}, ensure_ascii=False, indent=2))
        return

    # ── paginated modes ───────────────────────────────────────────────────────

    if args.mode == "projects":
        endpoint = build_api_url(base_url, "rest/api/3/project/search")
        params: dict = {"orderBy": "name", "expand": "description"}

    elif args.mode == "boards":
        endpoint = build_api_url(base_url, "rest/agile/1.0/board")
        params = {"projectKeyOrId": _project_key(config)}

    elif args.mode == "sprints":
        board_id = args.ref or str(config.get("defaultBoardId", "")).strip()
        if not board_id:
            fail(
                "sprints mode requires a board id",
                details={
                    "usage": "jira_lookup_metadata.py <config> sprints <boardId>  "
                    "(or set defaultBoardId in config)"
                },
            )
        endpoint = build_api_url(base_url, f"rest/agile/1.0/board/{board_id}/sprint")
        params = {"state": "active,future"}

    elif args.mode == "members":
        endpoint = build_api_url(base_url, "rest/api/3/user/assignable/search")
        params = {"project": _project_key(config)}

    else:
        fail(f"unhandled mode: {args.mode}")
        return  # unreachable; satisfies type checkers

    items = fetch_all_pages(
        method="GET",
        endpoint=endpoint,
        headers=headers,
        params=params,
        page_size=args.page_size,
    )
    print(json.dumps({"ok": True, "mode": args.mode, "total": len(items), "data": items}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
