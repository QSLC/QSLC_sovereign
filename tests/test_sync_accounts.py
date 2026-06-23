from qslc_sync import default_account_state, sync_message, sync_status


def test_online_sync_status_live_when_all_accounts_connected():
    accounts = default_account_state(offline_mode=False)
    assert sync_status(accounts, offline_mode=False) == "Live"


def test_online_sync_status_attention_required_when_account_disconnected():
    accounts = default_account_state(offline_mode=False)
    accounts["google_sheets"] = False
    assert sync_status(accounts, offline_mode=False) == "Attention Required"
    assert "Google Sheets" in sync_message(accounts, offline_mode=False)


def test_offline_mode_forces_cached_state():
    accounts = {"snowflake": False, "google_sheets": False, "m365_vault": False, "icloud_master": False}
    assert sync_status(accounts, offline_mode=True) == "Cached"
    assert sync_message(accounts, offline_mode=True).startswith("Sync deferred.")
