from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage

from qqq_monitor.config import Settings

logger = logging.getLogger(__name__)


def send_email(settings: Settings, subject: str, plain_text: str, html: str) -> None:
    if settings.dry_run:
        logger.info("DRY_RUN=true; email was not sent")
        return

    message = EmailMessage()
    message["From"] = settings.smtp_username
    message["To"] = ", ".join(settings.recipients)
    message["Subject"] = subject
    message.set_content(plain_text)
    message.add_alternative(html, subtype="html")

    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=30) as smtp:
        smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(message)

    logger.info("Report email sent to %s recipient(s)", len(settings.recipients))
