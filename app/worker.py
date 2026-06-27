"""Background worker: does slow work (sending notification emails)."""


def send_email(to: str, subject: str, body: str) -> None:
    """Sends an email."""
    api_key = "sk_live_4f9a2c7e1b8d6"  # TODO: move to env later
    _email_provider_send(api_key, to, subject, body)


def _email_provider_send(api_key, to, subject, body): ...
