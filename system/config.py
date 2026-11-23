"""Central configuration for Agent OS.

Loads settings from the project-level `.env`, resolves every vault path used by
bridge, router and panel, and exposes BRT (America/Sao_Paulo) time helpers.

Secrets are loaded into memory only and are excluded from `repr()` so they never
leak into logs, reports or panel pages.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone, tzinfo
from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT_DIR: Path = Path(__file__).resolve().parent.parent
ENV_FILE: Path = ROOT_DIR / ".env"

# Values from `.env` never override variables already set in the process
# environment (useful for tests and for the Windows Task Scheduler).
load_dotenv(ENV_FILE, override=False)

DEFAULT_TZ_NAME = "America/Sao_Paulo"
PANEL_HOST = "127.0.0.1"
PANEL_PORT = 8000
PANEL_URL = f"http://{PANEL_HOST}:{PANEL_PORT}"

# Placeholders shipped in `.env.example`; treated as "not configured".
_PLACEHOLDER_PREFIXES = ("cole_", "opcional_")

METRIC_FILES = ("hoje", "projetos", "empresa", "financeiro", "custos-ia")


# ---------------------------------------------------------------------------
# Time helpers (BRT)
# ---------------------------------------------------------------------------
def _load_tz(name: str) -> tzinfo:
    """Return the IANA timezone, falling back to a fixed UTC-3 offset.

    Windows ships without the IANA database (it needs the `tzdata` package).
    Brazil abolished DST in 2019, so a fixed -03:00 offset is equivalent.
    """
    try:
        from zoneinfo import ZoneInfo

        return ZoneInfo(name)
    except Exception:  # ZoneInfoNotFoundError, ImportError
        return timezone(timedelta(hours=-3), name="BRT")


def now_brt() -> datetime:
    """Current aware datetime in the configured timezone (BRT by default)."""
    return datetime.now(get_settings().tz)


def today_brt() -> str:
    """Today's date as `YYYY-MM-DD` in BRT."""
    return now_brt().strftime("%Y-%m-%d")


def timestamp_brt(dt: datetime | None = None) -> str:
    """Timestamp in the vault standard format: `YYYY-MM-DD HH:MM BRT`."""
    dt = dt or now_brt()
    return dt.strftime("%Y-%m-%d %H:%M") + " BRT"


def hhmm_brt(dt: datetime | None = None) -> str:
    """Hour and minute (`HH:MM`) in BRT, used in the request log lines."""
    return (dt or now_brt()).strftime("%H:%M")


# ---------------------------------------------------------------------------
# Env parsing helpers
# ---------------------------------------------------------------------------
def _env_str(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _env_secret(name: str) -> str:
    value = _env_str(name)
    if not value or value.lower().startswith(_PLACEHOLDER_PREFIXES):
        return ""
    return value


def _env_float(name: str, default: float) -> float:
    raw = _env_str(name)
    if not raw:
        return default
    try:
        return float(raw.replace(",", "."))
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    raw = _env_str(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _resolve_path(raw: str, default: str) -> Path:
    path = Path(raw or default).expanduser()
    if not path.is_absolute():
        path = ROOT_DIR / path
    return path.resolve()


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Settings:
    tz_name: str
    tz: tzinfo = field(repr=False)
    vault_path: Path
    repos_config_path: Path

    # Router level 2 (cloud)
    n2_provider: str
    n2_model: str
    gemini_api_key: str = field(repr=False)
    anthropic_api_key: str = field(repr=False)

    # Router level 3 (Claude Code headless)
    claude_cli: str

    # Daily cost control
    daily_budget_usd: float
    daily_n2_limit_calls: int
    daily_n3_limit_calls: int
    cost_alert_threshold: float

    # Telegram
    telegram_bot_token: str = field(repr=False)
    telegram_chat_id: str = field(repr=False)

    # --- Vault layout -----------------------------------------------------
    @property
    def raw_dir(self) -> Path:
        return self.vault_path / "raw"

    @property
    def wiki_dir(self) -> Path:
        return self.vault_path / "wiki"

    @property
    def projetos_dir(self) -> Path:
        return self.vault_path / "projetos"

    @property
    def outputs_dir(self) -> Path:
        return self.vault_path / "outputs"

    @property
    def specs_dir(self) -> Path:
        return self.outputs_dir / "specs"

    @property
    def relatorios_dir(self) -> Path:
        return self.outputs_dir / "relatorios"

    @property
    def metricas_dir(self) -> Path:
        return self.outputs_dir / "metricas"

    @property
    def logs_dir(self) -> Path:
        return self.vault_path / "logs"

    @property
    def logs_pedidos_dir(self) -> Path:
        return self.logs_dir / "pedidos"

    @property
    def logs_router_dir(self) -> Path:
        return self.logs_dir / "router"

    @property
    def logs_automacoes_dir(self) -> Path:
        return self.logs_dir / "automacoes"

    @property
    def skills_dir(self) -> Path:
        return self.vault_path / "skills"

    @property
    def claude_md(self) -> Path:
        return ROOT_DIR / "CLAUDE.md"

    def metric_path(self, name: str) -> Path:
        """Path to `vault/outputs/metricas/<name>.json`."""
        return self.metricas_dir / f"{name}.json"

    # --- Capability flags (never expose the secret values) ----------------
    @property
    def n2_api_key(self) -> str:
        if self.n2_provider == "anthropic":
            return self.anthropic_api_key
        return self.gemini_api_key

    @property
    def n2_configured(self) -> bool:
        return self.n2_provider in {"gemini", "anthropic"} and bool(self.n2_api_key)

    @property
    def telegram_configured(self) -> bool:
        return bool(self.telegram_bot_token and self.telegram_chat_id)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Build settings once per process from the environment / `.env`."""
    tz_name = _env_str("TZ", DEFAULT_TZ_NAME) or DEFAULT_TZ_NAME
    provider = _env_str("N2_PROVIDER", "gemini").lower()
    default_model = "claude-haiku-4-5-20251001" if provider == "anthropic" else "gemini-2.5-flash"
    return Settings(
        tz_name=tz_name,
        tz=_load_tz(tz_name),
        vault_path=_resolve_path(_env_str("VAULT_PATH"), "./vault"),
        repos_config_path=_resolve_path(_env_str("REPOS_CONFIG_PATH"), "./system/bridge/repos.json"),
        n2_provider=provider,
        n2_model=_env_str("N2_MODEL", default_model) or default_model,
        gemini_api_key=_env_secret("GEMINI_API_KEY"),
        anthropic_api_key=_env_secret("ANTHROPIC_API_KEY"),
        claude_cli=_env_str("CLAUDE_CLI", "claude") or "claude",
        daily_budget_usd=_env_float("DAILY_BUDGET_USD", 2.00),
        daily_n2_limit_calls=_env_int("DAILY_N2_LIMIT_CALLS", 100),
        daily_n3_limit_calls=_env_int("DAILY_N3_LIMIT_CALLS", 25),
        cost_alert_threshold=_env_float("COST_ALERT_THRESHOLD", 0.80),
        telegram_bot_token=_env_secret("TELEGRAM_BOT_TOKEN"),
        telegram_chat_id=_env_secret("TELEGRAM_CHAT_ID"),
    )


# ---------------------------------------------------------------------------
# JSON helpers shared by bridge, router and panel
# ---------------------------------------------------------------------------
def read_json(path: Path, default: Any = None) -> Any:
    """Read a JSON file; return `default` if it is missing or invalid."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def write_json(path: Path, data: Any) -> None:
    """Atomically write pretty UTF-8 JSON (keeps accents readable)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


if __name__ == "__main__":
    s = get_settings()
    print("Agent OS — configuração carregada")
    print(f"  Raiz:              {ROOT_DIR}")
    print(f"  Vault:             {s.vault_path} (existe: {s.vault_path.is_dir()})")
    print(f"  Fuso:              {s.tz_name} -> {timestamp_brt()}")
    print(f"  Nível 2:           {s.n2_provider} / {s.n2_model} (chave configurada: {s.n2_configured})")
    print(f"  Nível 3:           {s.claude_cli} -p")
    print(f"  Limite diário:     US$ {s.daily_budget_usd:.2f} | N2 {s.daily_n2_limit_calls} | N3 {s.daily_n3_limit_calls} chamadas")
    print(f"  Alerta de custo:   {s.cost_alert_threshold:.0%}")
    print(f"  Telegram:          configurado: {s.telegram_configured}")
    print(f"  Painel:            {PANEL_URL}")
