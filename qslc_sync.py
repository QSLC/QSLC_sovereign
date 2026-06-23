"""Core account and sync state helpers for Node 1010 dashboard."""

from __future__ import annotations

from typing import Dict, Iterable

ACCOUNT_LABELS = {
    "snowflake": "Snowflake",
    "google_sheets": "Google Sheets",
    "m365_vault": "Microsoft 365 Vault",
    "icloud_master": "iCloud Master Vault",
}


def default_account_state(offline_mode: bool) -> Dict[str, bool]:
    if offline_mode:
        return {key: True for key in ACCOUNT_LABELS}
    return {
        "snowflake": True,
        "google_sheets": True,
        "m365_vault": True,
        "icloud_master": True,
    }


def disconnected_accounts(accounts: Dict[str, bool]) -> Iterable[str]:
    return [ACCOUNT_LABELS[key] for key, connected in accounts.items() if not connected]


def sync_status(accounts: Dict[str, bool], offline_mode: bool) -> str:
    if offline_mode:
        return "Cached"
    return "Live" if not list(disconnected_accounts(accounts)) else "Attention Required"


def sync_message(accounts: Dict[str, bool], offline_mode: bool) -> str:
    if offline_mode:
        return "Sync deferred. Data preserved in localized hardware vault."

    missing = list(disconnected_accounts(accounts))
    if missing:
        return (
            "Sync blocked. Reconnect required accounts: "
            + ", ".join(missing)
            + "."
        )
    return "Bi-directional sync complete: Snowflake 🔄 Google Sheets 🔄 M365 Asset Vault 🔄 iCloud Master Vault."
