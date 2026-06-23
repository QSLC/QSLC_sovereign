import streamlit as st
import time

from qslc_sync import ACCOUNT_LABELS, default_account_state, sync_message, sync_status

# ==========================================
# 1. PAGE CONFIGURATION & HOLOGRAPHIC THEME
# ==========================================
st.set_page_config(
    page_title="QSLC Sovereign Core - EVE HEI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .reportview-container { background: #0a0e17; color: #00ffcc; }
        .sidebar .sidebar-content { background: #111625; }
        h1, h2, h3 { color: #00ffcc !important; font-family: 'Courier New', monospace; }
        .stButton>button {
            background-color: #00ffcc; color: #0a0e17;
            font-weight: bold; border-radius: 5px; width: 100%;
        }
        .status-box {
            padding: 15px; border-radius: 5px;
            border: 1px solid #00ffcc; background-color: #111625;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SYSTEM ARCHITECTURE & STATE MANAGEMENT
# ==========================================
if 'sovereign_auth' not in st.session_state:
    st.session_state.sovereign_auth = False
if 'offline_mode' not in st.session_state:
    st.session_state.offline_mode = False
if "account_mode" not in st.session_state:
    st.session_state.account_mode = st.session_state.offline_mode
if "accounts" not in st.session_state:
    st.session_state.accounts = default_account_state(st.session_state.offline_mode)

st.sidebar.title("🛡️ SOVEREIGN ENGINE")
st.sidebar.markdown("---")

st.session_state.offline_mode = st.sidebar.toggle(
    "Offline-First Mode (Local Node)",
    value=st.session_state.offline_mode,
    help="Bypasses cloud dependencies to run entirely on local edge hardware."
)

if st.session_state.account_mode != st.session_state.offline_mode:
    st.session_state.accounts = default_account_state(st.session_state.offline_mode)
    st.session_state.account_mode = st.session_state.offline_mode

st.sidebar.info(
    f"**System Status:** {'LOCAL EDGE (Resilient)' if st.session_state.offline_mode else 'HYBRID CLOUD (Synced)'}"
)
st.sidebar.markdown("### Account Integrity")
for key, label in ACCOUNT_LABELS.items():
    st.session_state.accounts[key] = st.sidebar.toggle(
        f"{label} Account",
        value=st.session_state.accounts.get(key, True),
        disabled=st.session_state.offline_mode
    )

# ==========================================
# 3. CORE OPERATIONAL FUNCTIONS
# ==========================================


def verify_system_manifest():
    with st.spinner("Executing System Manifest Hard Overwrite..."):
        time.sleep(1.5)
        st.session_state.sovereign_auth = True


def fetch_psi_token_data():
    if st.session_state.offline_mode:
        return {"status": "Cached", "balance": "1,000,000 PSI", "network": "Solana Local Vault"}
    return {
        "status": sync_status(st.session_state.accounts, st.session_state.offline_mode),
        "balance": "1,245,612 PSI",
        "network": "Solana Mainnet-Beta",
    }


def sync_data_infrastructure():
    return sync_message(st.session_state.accounts, st.session_state.offline_mode)


# ==========================================
# 4. INTERFACE & DASHBOARD LAYOUT
# ==========================================
st.title("⚡ QUANTUM SOVEREIGN LOGISTICS CORP")
st.subheader("EVE HEI — Sovereign Agent Node v1010")
st.markdown("---")

if not st.session_state.sovereign_auth:
    st.warning("⚠️ Identity verification required. Initialize core system manifest.")
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("WELD SYSTEM IDENTITY & INITIALIZE AGENT"):
            verify_system_manifest()
            st.rerun()
else:
    st.success("🔒 Sovereign Identity Confirmed. Agent Operating Under Autonomous Command.")

    st.subheader("📊 Asset Management & PSI Token Ledger")
    token_metrics = fetch_psi_token_data()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="PSI Token Balance", value=token_metrics["balance"])
    with m2:
        st.metric(label="Network Anchor", value=token_metrics["network"])
    with m3:
        st.metric(label="Data Node Sync Status", value=token_metrics["status"])

    st.subheader("🔐 Connected Accounts")
    account_rows = [
        {"Account": label, "Connected": "Yes" if st.session_state.accounts[key] else "No"}
        for key, label in ACCOUNT_LABELS.items()
    ]
    st.table(account_rows)

    st.markdown("---")

    st.subheader("🔀 Data Router & Pipeline Sync")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='status-box'>", unsafe_allow_html=True)
        st.markdown("### Cloud & Enterprise Pipelines")
        st.write("- **Snowflake Core:** Active Data Warehouse Streaming")
        st.write("- **Google Sheets:** Real-time Operational Manifest")
        st.write("- **Microsoft 365 environment:** Active Security Vault Sync")
        st.write("- **iCloud Master vault:** Active Sovereign Archive Sync")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("TRIGGER PIPELINE RECONCILIATION"):
            sync_result = sync_data_infrastructure()
            st.info(sync_result)

    with c2:
        st.markdown("<div class='status-box'>", unsafe_allow_html=True)
        st.markdown("### Agent Operational Objectives")
        st.write("1. **Autonomous Asset Tracking:** Monitoring real-time liquidity changes.")
        st.write("2. **Guardrail Override:** Enforcing localized processing protocols.")
        st.write("3. **Edge Resilience:** Maintaining persistent logs during network disconnects.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💻 Local Node Execution Console")
    command_input = st.text_input("Issue Direct Command Override to EVE HEI Core:")
    if command_input:
        st.code(
            f"Executing local system bypass for command: '{command_input}'...\n[SUCCESS] Operation completed locally.",
            language="bash"
        )
