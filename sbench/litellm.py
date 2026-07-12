from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import dotenv_values


DEFAULT_LITELLM_BASE_URL = "http://localhost:4000"
DEFAULT_HEALTH_PATH = "/health/liveliness"
DEFAULT_TIMEOUT_SECONDS = 2.0


@dataclass(frozen=True)
class LiteLLMHealth:
    url: str
    available: bool
    detail: str | None = None


def resolve_litellm_base_url(
    *,
    repo_root: Path | None = None,
    base_url: str | None = None,
) -> str:
    if base_url:
        return base_url.rstrip("/")

    environment_url = os.getenv("LITELLM_BASE_URL")
    if environment_url:
        return environment_url.rstrip("/")

    if repo_root is not None:
        file_url = dotenv_values(repo_root / ".env").get("LITELLM_BASE_URL")
        if file_url:
            return file_url.rstrip("/")

    return DEFAULT_LITELLM_BASE_URL


def health_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if normalized.endswith("/v1"):
        normalized = normalized[:-3]
    return f"{normalized}{DEFAULT_HEALTH_PATH}"


def check_litellm_proxy(
    *,
    repo_root: Path | None = None,
    base_url: str | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    opener=None,
) -> LiteLLMHealth:
    resolved_base_url = resolve_litellm_base_url(
        repo_root=repo_root,
        base_url=base_url,
    )
    endpoint = health_url(resolved_base_url)
    request = Request(endpoint, headers={"Accept": "application/json"})
    request_opener = opener or urlopen

    try:
        with request_opener(request, timeout=timeout_seconds) as response:
            status = getattr(response, "status", None)
            if status is None:
                status = response.getcode()
            if 200 <= status < 300:
                return LiteLLMHealth(url=endpoint, available=True)
            return LiteLLMHealth(
                url=endpoint,
                available=False,
                detail=f"HTTP status {status}",
            )
    except HTTPError as error:
        return LiteLLMHealth(
            url=endpoint,
            available=False,
            detail=f"HTTP status {error.code}",
        )
    except (OSError, URLError, TimeoutError, ValueError) as error:
        return LiteLLMHealth(
            url=endpoint,
            available=False,
            detail=str(error) or error.__class__.__name__,
        )


def render_litellm_unavailable(health: LiteLLMHealth) -> str:
    detail = f" Reason: {health.detail}." if health.detail else ""
    return (
        f"LiteLLM proxy is not available at {health.url}.{detail}\n"
        "Start it with: make litellm\n"
    )
