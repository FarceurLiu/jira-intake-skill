#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any, Dict

from _jira_common import build_api_url, build_headers, fail, get_base_url, load_team_config, request_json, text_to_adf_document


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post a comment to an existing Jira issue.")
    parser.add_argument("config_path", help="path to team-config JSON file")
    parser.add_argument("issue_key", help="Jira issue key, e.g. APP-123")
    parser.add_argument("--comment-file", required=True, help="path to a UTF-8 text or JSON ADF file")
    parser.add_argument(
        "--format",
        choices=("auto", "text", "adf"),
        default="auto",
        help="comment-file format; auto treats .json as ADF and other extensions as plain text",
    )
    parser.add_argument("--dry-run", action="store_true", help="prepare body but do not post to Jira")
    return parser.parse_args()


def load_comment_body(path: Path, fmt: str) -> Dict[str, Any]:
    """Load and parse a comment file into an ADF document dict.

    *fmt* may be ``"auto"`` (infer from file extension), ``"text"``, or
    ``"adf"``.  Plain text is converted via ``text_to_adf_document``.
    JSON files are expected to already be valid ADF objects.
    """
    if not path.is_file():
        fail(f"comment file not found: {path}")

    detected = fmt
    if fmt == "auto":
        detected = "adf" if path.suffix.lower() == ".json" else "text"

    raw = path.read_text(encoding="utf-8")
    if detected == "adf":
        try:
            body = json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(
                f"invalid ADF JSON comment file: {path}",
                details={"error": str(exc), "path": str(path)},
            )
        if not isinstance(body, dict):
            fail(f"ADF comment body must be a JSON object, got {type(body).__name__}: {path}")
        return body  # type: ignore[return-value]

    return text_to_adf_document(raw)


def main() -> None:
    args = parse_args()
    config = load_team_config(args.config_path)
    comment_body = load_comment_body(Path(args.comment_file), args.format)

    result: Dict[str, Any] = {
        "ok": True,
        "issue": args.issue_key,
        "commentFile": args.comment_file,
        "dryRun": args.dry_run,
        "body": comment_body,
    }

    if not args.dry_run:
        headers = build_headers(config, include_content_type=True)
        base_url = get_base_url(config)
        response = request_json(
            method="POST",
            url=build_api_url(base_url, f"rest/api/3/issue/{args.issue_key}/comment"),
            headers=headers,
            payload={"body": comment_body},
        )
        result["response"] = response

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
