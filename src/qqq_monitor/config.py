import os
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo


class ConfigurationError(RuntimeError):
    """Raised when required runtime configuration is missing."""


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    symbol: str
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    recipients: tuple[str, ...]
    timezone: ZoneInfo
    output_dir: Path
    dry_run: bool

    @classmethod
    def from_env(cls) -> "Settings":
        dry_run = _env_bool("DRY_RUN", default=False)
        username = os.getenv("SMTP_USERNAME", "").strip()
        password = os.getenv("SMTP_PASSWORD", "").strip()
        recipients = tuple(
            email.strip()
            for email in os.getenv("RECEIVER_EMAILS", "").split(",")
            if email.strip()
        )

        if not dry_run:
            missing = []
            if not username:
                missing.append("SMTP_USERNAME")
            if not password:
                missing.append("SMTP_PASSWORD")
            if not recipients:
                missing.append("RECEIVER_EMAILS")
            if missing:
                raise ConfigurationError(
                    "Missing required environment variables: " + ", ".join(missing)
                )

        try:
            timezone = ZoneInfo(os.getenv("REPORT_TIMEZONE", "Asia/Shanghai"))
            smtp_port = int(os.getenv("SMTP_PORT", "465"))
        except (ValueError, KeyError) as exc:
            raise ConfigurationError(f"Invalid runtime configuration: {exc}") from exc

        return cls(
            symbol=os.getenv("SYMBOL", "QQQ").strip().upper(),
            smtp_host=os.getenv("SMTP_HOST", "smtp.qq.com").strip(),
            smtp_port=smtp_port,
            smtp_username=username,
            smtp_password=password,
            recipients=recipients,
            timezone=timezone,
            output_dir=Path(os.getenv("OUTPUT_DIR", "output")),
            dry_run=dry_run,
        )
