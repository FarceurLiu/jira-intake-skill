#!/usr/bin/env python3
import base64
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib import error, parse, request


# Retry attempts for transient Jira failures (HTTP 429 / 5xx).
DEFAULT_RETRY = 4
# Per-request socket timeout in seconds; covers slow Jira Cloud responses.
DEFAULT_TIMEOUT = 45


def fail(message: str, *, details: Optional[Any] = None, exit_code: int = 1) -> None:
    """Print a JSON error payload to stdout and exit."""
    payload: Dict[str, Any] = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code)


def load_json(path: str) -> Any:
    """Load and parse a JSON file.

    Raises distinct errors for missing file vs. malformed JSON so callers
    can tell the difference at a glance.
    """
    resolved = Path(path).resolve()
    try:
        with open(resolved, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        fail(f"file not found: {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in file: {path}", details=str(exc))


def _parse_dotenv(env_file: Path) -> None:
    """Read a .env file and populate missing environment variables.

    Rules:
    - Lines starting with ``#`` are comments and are skipped.
    - Empty lines are skipped.
    - Format: ``KEY=value`` or ``KEY="value"`` or ``KEY='value'``.
    - Surrounding single or double quotes are stripped from values.
    - Variables that are **already set** in the environment are NOT
      overwritten — the real environment always takes priority.
    - Read errors are silently ignored; .env is always optional.
    """
    try:
        for raw_line in env_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # Strip matching surrounding quotes
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            if key and key not in os.environ:
                os.environ[key] = value
    except OSError:
        pass  # .env is optional — silently ignore any read errors


def _load_dotenv(config_path: str) -> None:
    """Look for a .env file and load it into the environment.

    Search order (stops at first match):
    1. Same directory as *config_path* — so ``config/.env`` works when
       the config file lives in ``config/``.
    2. Current working directory.

    This means users can place a ``.env`` file next to their private
    config file and never have to set environment variables manually.
    """
    search_dirs = [
        Path(config_path).resolve().parent,
        Path.cwd(),
    ]
    seen: set = set()
    for directory in search_dirs:
        if directory in seen:
            continue
        seen.add(directory)
        candidate = directory / ".env"
        if candidate.is_file():
            _parse_dotenv(candidate)
            break


def load_team_config(path: str) -> Dict[str, Any]:
    """Load a team-config JSON file and verify it is a JSON object.

    Also loads a ``.env`` file from the same directory (or CWD) so that
    the API token can be stored in a plain text file instead of requiring
    the user to set environment variables manually.
    """
    _load_dotenv(path)
    config = load_json(path)
    if not isinstance(config, dict):
        fail(f"team config must be a JSON object, got {type(config).__name__}: {path}")
    return config  # type: ignore[return-value]


def get_base_url(config: Dict[str, Any]) -> str:
    """Extract and validate the Jira base URL from a team config dict.

    Strips trailing slashes so callers can safely append paths with
    ``build_api_url`` or an f-string.
    """
    base_url = str(config.get("baseUrl", "")).strip().rstrip("/")
    if not base_url:
        fail("missing baseUrl in team config")
    return base_url


def build_api_url(base_url: str, endpoint: str) -> str:
    """Join a base URL with a REST API endpoint path.

    Normalises leading/trailing slashes so double-slash and missing-slash
    edge cases cannot occur.

    Example::

        build_api_url("https://x.atlassian.net", "rest/api/3/issue/APP-1")
        # → "https://x.atlassian.net/rest/api/3/issue/APP-1"
    """
    return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"


def build_headers(config: Dict[str, Any], *, include_content_type: bool = False) -> Dict[str, str]:
    """Build the HTTP headers required for Jira Cloud Basic Auth."""
    base_url = str(config.get("baseUrl", "")).strip()
    email = str(config.get("email", "")).strip()
    api_token_env = _api_token_env_name(config)
    api_token = os.getenv(api_token_env, "").strip()
    if not base_url or not email or not api_token:
        fail(
            "missing Jira baseUrl/email/token",
            details={"required": ["baseUrl", "email", api_token_env]},
        )
    auth = base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("ascii")
    headers = {
        "Authorization": "Basic " + auth,
        "Accept": "application/json",
    }
    if include_content_type:
        headers["Content-Type"] = "application/json"
    return headers


def _api_token_env_name(config: Dict[str, Any]) -> str:
    """Return the env-var name that holds the Jira API token."""
    return str(config.get("apiTokenEnv", "JIRA_API_TOKEN")).strip() or "JIRA_API_TOKEN"


def _should_retry_http(status_code: int) -> bool:
    return status_code == 429 or status_code >= 500


def request_json(
    *,
    method: str,
    url: str,
    headers: Dict[str, str],
    payload: Optional[Any] = None,
    retry: int = DEFAULT_RETRY,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """Make an HTTP request and return the parsed JSON response.

    Retries automatically on HTTP 429 and 5xx with exponential back-off.
    Calls ``fail()`` (and exits) on non-retryable errors.
    """
    data: Optional[bytes] = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    last_exc: Optional[Exception] = None
    for attempt in range(retry):
        try:
            req = request.Request(url, headers=headers, method=method.upper(), data=data)
            with request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                if not raw.strip():
                    return {"ok": True, "status": resp.status}
                parsed = json.loads(raw)
                if isinstance(parsed, dict):
                    return parsed
                return {"ok": True, "data": parsed, "status": resp.status}
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", "ignore")
            if not _should_retry_http(exc.code):
                fail(
                    f"Jira API error {exc.code} for {method.upper()} {url}",
                    details=_safe_json_or_text(body),
                )
            last_exc = exc
        except (error.URLError, ConnectionResetError, OSError) as exc:
            last_exc = exc

        if attempt < retry - 1:
            time.sleep(2 ** (attempt + 1))

    fail(
        f"Jira API request failed after {retry} attempts for {method.upper()} {url}",
        details=str(last_exc) if last_exc else None,
    )


def _safe_json_or_text(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def fetch_all_pages(
    *,
    method: str,
    endpoint: str,
    headers: Dict[str, str],
    params: Optional[Dict[str, Any]] = None,
    page_size: int = 50,
    retry: int = DEFAULT_RETRY,
    timeout: int = DEFAULT_TIMEOUT,
) -> List[Any]:
    """Auto-paginate any Jira REST endpoint that uses startAt/maxResults.

    Handles two response shapes:

    Object  ``{"values": [...], "total": N, "isLast": bool, ...}``
            Used by: project/search, agile board, agile sprint.

    Array   ``[...]`` — request_json wraps it as ``{"ok": True, "data": [...]}``
            Used by: user/assignable/search (no "total" field).
            Stops when the returned page is shorter than page_size.

    Returns a flat list of all collected items across all pages.
    Calls ``fail()`` if the response shape is neither of the above.
    """
    all_items: List[Any] = []
    start_at = 0
    base_params: Dict[str, Any] = dict(params or {})

    while True:
        page_params = {**base_params, "startAt": start_at, "maxResults": page_size}
        url = f"{endpoint}?{parse.urlencode(page_params)}"
        raw = request_json(method=method, url=url, headers=headers, retry=retry, timeout=timeout)

        # ── Array response (wrapped by request_json) ──────────────────────────
        if "data" in raw and isinstance(raw["data"], list):
            page: List[Any] = raw["data"]
            all_items.extend(page)
            if len(page) < page_size:
                break
            start_at += len(page)

        # ── Object response with "values" list ────────────────────────────────
        elif "values" in raw:
            page = raw.get("values", [])
            all_items.extend(page)
            if raw.get("isLast", False):
                break
            total = raw.get("total")
            if total is not None and start_at + len(page) >= total:
                break
            if not page:  # empty page guard — prevents infinite loop
                break
            start_at += len(page)

        else:
            fail(
                "fetch_all_pages: unexpected response shape — neither 'values' nor array 'data' found",
                details={
                    "endpoint": endpoint,
                    "startAt": start_at,
                    "responseKeys": list(raw.keys()),
                },
            )

    return all_items


def normalize_text(value: str) -> str:
    """Collapse whitespace and lowercase a string for fuzzy matching."""
    return "".join(str(value).lower().split())


def text_to_adf_document(text: str) -> Dict[str, Any]:
    """Convert plain text to an Atlassian Document Format (ADF) document.

    Blank lines are treated as paragraph separators. Single newlines within
    a paragraph become hard line breaks.

    An empty or whitespace-only *text* returns a single empty paragraph —
    the minimum valid ADF document body accepted by Jira Cloud REST v3.
    """
    paragraphs = []
    for raw_block in text.replace("\r\n", "\n").split("\n\n"):
        block = raw_block.strip("\n")
        if not block.strip():
            continue
        lines = block.split("\n")
        content: List[Dict[str, Any]] = []
        for index, line in enumerate(lines):
            if line:
                content.append({"type": "text", "text": line})
            if index < len(lines) - 1:
                content.append({"type": "hardBreak"})
        paragraphs.append({"type": "paragraph", "content": content or [{"type": "text", "text": ""}]})

    return {
        "type": "doc",
        "version": 1,
        "content": paragraphs or [{"type": "paragraph", "content": [{"type": "text", "text": ""}]}],
    }


def resolve_transition_id(
    *,
    config: Dict[str, Any],
    issue_key: str,
    transition_ref: str,
) -> str:
    """Resolve a transition reference to a numeric Jira transition id.

    Accepts a numeric id string, a logical key from ``statusTransitionMap``
    in the config, or a status name / untranslated name from the Jira API.
    Calls ``fail()`` if the reference cannot be resolved.
    """
    transition_value = transition_ref.strip()
    mapped = config.get("statusTransitionMap", {}).get(transition_value)
    if isinstance(mapped, str) and mapped.strip():
        transition_value = mapped.strip()

    if transition_value.isdigit():
        return transition_value

    headers = build_headers(config)
    base_url = get_base_url(config)
    response = request_json(
        method="GET",
        url=build_api_url(base_url, f"rest/api/3/issue/{issue_key}/transitions"),
        headers=headers,
    )
    transitions = response.get("transitions", [])
    target = normalize_text(transition_value)
    for transition in transitions:
        candidates = [
            str(transition.get("id", "")),
            str(transition.get("name", "")),
            str(transition.get("to", {}).get("name", "")),
            str(transition.get("to", {}).get("untranslatedName", "")),
        ]
        if any(normalize_text(candidate) == target for candidate in candidates if candidate):
            transition_id = str(transition.get("id", "")).strip()
            if transition_id:
                return transition_id

    fail(
        f"cannot resolve transition '{transition_ref}' for {issue_key}",
        details={"availableTransitions": transitions},
    )
