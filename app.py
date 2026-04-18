import streamlit as st
import pandas as pd
from datetime import date, datetime

import database as db
import analysis as an
import charts as ch

# Page config 
st.set_page_config(
    page_title="Finance Tracker",
    
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Clean card style */
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 18px 20px;
        margin-bottom: 10px;
        border-left: 4px solid #4CAF50;
        color: #000000;
    }
    .metric-card.red  { border-left-color: #F44336; }
    .metric-card.blue { border-left-color: #2196F3; }
    .metric-card.orange { border-left-color: #FF9800; }

    .judge-good     { background:#e8f5e9; border-radius:8px; padding:10px 14px; margin:6px 0; color: #000000; }
    .judge-ok       { background:#fff8e1; border-radius:8px; padding:10px 14px; margin:6px 0; color: #000000; }
    .judge-bad      { background:#ffebee; border-radius:8px; padding:10px 14px; margin:6px 0; color: #000000; }
    .judge-critical { background:#fce4ec; border-radius:8px; padding:10px 14px; margin:6px 0; border:1px solid #e91e63; color: #000000; }
    .judge-info     { background:#e3f2fd; border-radius:8px; padding:10px 14px; margin:6px 0; color: #000000; }

    .suggest-box { background:#f3f4f6; border-radius:8px; padding:12px 16px; margin:6px 0; font-size:14px; color: #000000; }
    h1 { font-size: 1.8rem !important; }
    .stTabs [data-baseweb="tab"] { font-size: 15px; font-weight: 500; }
    
    /* Hide number input spinner buttons */
    input[type=number]::-webkit-outer-spin-button,
    input[type=number]::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    input[type=number] {
        -moz-appearance: textfield;
    }
</style>
""", unsafe_allow_html=True)

#Init DB
db.init_db()

# Sidebar 
with st.sidebar:
    st.title("Finance Tracker")
    st.markdown("---")
    st.subheader("Add Transaction")

    with st.form("add_form", clear_on_submit=True):
        t_date  = st.date_input("Date", value=date.today())
        t_type  = st.selectbox("Type", ["expense", "income"])
        
        if t_type == "expense":
            cat_options = ["food", "rent", "utilities", "healthcare", "transport",
                           "shopping", "entertainment", "dining out", "travel",
                           "subscriptions", "stocks", "mutual funds", "fd", "crypto", "other"]
        else:
            cat_options = ["salary", "freelance", "business", "dividends", "other"]
        
        t_cat   = st.selectbox("Category", cat_options)
        t_amt   = st.number_input("Amount (₹)", min_value=1, step=1)
        t_note  = st.text_input("Note (optional)")
        submit  = st.form_submit_button("Add", use_container_width=True)

        if submit and t_amt > 0:
            db.add_transaction(str(t_date), t_type, t_cat, t_amt, t_note)
            st.success("Saved!")

    st.markdown("---")
    st.caption("Smart Finance Tracker | Built with Streamlit")

# Load data
df = db.get_all_transactions()

# Header
st.title("Smart Finance Tracker")
st.markdown("Track. Analyse. Improve your financial health.")


if df.empty:
    st.info("No data yet. Add your first transaction in the sidebar to get started!")
    st.stop()

# ── Tabs
tabs = st.tabs(["Dashboard", "Analysis", "Health Score", "AI Suggestions", "Transactions"])


# TAB 1 — Dashboard

with tabs[0]:
    # Filter by month
    df["date"] = pd.to_datetime(df["date"])
    years  = sorted(df["date"].dt.year.unique(), reverse=True)
    months = list(range(1, 13))
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    c1, c2 = st.columns([1, 3])
    with c1:
        sel_year  = st.selectbox("Year",  years, key="dash_year")
        sel_month = st.selectbox("Month", months, format_func=lambda m: month_names[m-1], key="dash_month")

    filtered = df[
        (df["date"].dt.year  == sel_year) &
        (df["date"].dt.month == sel_month)
    ]

    metrics = an.compute_metrics(filtered)

    if not metrics or metrics["total_income"] == 0:
        st.warning("No income recorded for this month. Add income to see full analysis.")

    # KPI cards
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Income",  f"₹{metrics.get('total_income',0):,.0f}")
    k2.metric("Total Expenses", f"₹{metrics.get('total_expense',0):,.0f}")
    k3.metric("Savings",        f"₹{metrics.get('savings',0):,.0f}")
    k4.metric("Savings Rate",   f"{metrics.get('savings_rate',0)}%")

    st.markdown("---")

    # Charts
    col_a, col_b = st.columns(2)
    with col_a:
        cat_totals = metrics.get("cat_totals", {})
        if cat_totals:
            fig = ch.pie_chart(cat_totals, f"Expense Breakdown — {month_names[sel_month-1]} {sel_year}")
            st.pyplot(fig)
    with col_b:
        fig2 = ch.bar_chart(df, sel_year, sel_month)
        st.pyplot(fig2)

    # Spending breakdown table
    st.subheader("Category Summary")
    if not filtered.empty:
        summary = filtered.groupby(["type","category"])["amount"].sum().reset_index()
        summary.columns = ["Type", "Category", "Amount (₹)"]
        summary["Amount (₹)"] = summary["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(summary, use_container_width=True, hide_index=True)



# TAB 2 — Spending Analysis

with tabs[1]:
    st.subheader("Smart Spending Analysis")
    st.markdown("How does your spending behaviour look?")

    all_metrics = an.compute_metrics(df)

    # Overall ratios
    r1, r2, r3 = st.columns(3)
    r1.metric("Essential Spend",     f"{all_metrics.get('essential_rate',0)}%",  help="Target: ≤ 50% of income")
    r2.metric("Investment Rate",      f"{all_metrics.get('investment_rate',0)}%", help="Target: 10–30% of income")
    r3.metric("Discretionary Spend",  f"{all_metrics.get('non_ess_rate',0)}%",   help="Target: ≤ 20% of income")

    st.markdown("---")
    st.subheader("Behaviour Judgements")

    judgements = an.spending_judgements(all_metrics)
    for emoji, msg, sev in judgements:
        st.markdown(f'<div class="judge-{sev}">{emoji} {msg}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Category Trend")
    all_cats = sorted(df[df["type"]=="expense"]["category"].unique()) if not df.empty else []
    if all_cats:
        sel_cat = st.selectbox("Select category to view trend", all_cats)
        fig3 = ch.category_trend(df, sel_cat)
        if fig3:
            st.pyplot(fig3)

    # 50/20/30 rule reference
    st.markdown("---")
    st.subheader("The Ideal Budget Rule")
    inc = all_metrics.get("total_income", 0)
    if inc:
        col1, col2, col3 = st.columns(3)
        col1.metric("Essentials (50%)",    f"₹{inc*0.5:,.0f}")
        col2.metric("Savings (20%)",        f"₹{inc*0.2:,.0f}")
        col3.metric("Investments (30%)",    f"₹{inc*0.3:,.0f}")
        st.caption("Based on the popular 50/20/30 budgeting framework")



# TAB 3 — Health Score

with tabs[2]:
    st.subheader("Financial Health Score")
    st.markdown("A score from **0 to 100** based on your savings, spending and investment habits.")

    all_metrics = an.compute_metrics(df)
    score, pillars = an.compute_health_score(all_metrics)

    g1, g2 = st.columns([1, 1.4])
    with g1:
        fig_g = ch.health_gauge(score)
        st.pyplot(fig_g)
        if score >= 80:
            st.success("Excellent financial health! Keep it up.")
        elif score >= 50:
            st.warning("Room for improvement. Follow the suggestions tab.")
        else:
            st.error("Financial health is at risk. Take action now!")

    with g2:
        fig_p = ch.pillar_bar(pillars)
        st.pyplot(fig_p)
        st.markdown("**Scoring criteria (each pillar max 25)**")
        st.markdown("""
- **Savings Rate** — Are you saving ≥ 20% of income?  
- **Investment Mix** — Is investment in the 10–30% sweet spot?  
- **Essential Spend** — Are essentials ≤ 50% of income?  
- **Discretionary** — Is fun-spending kept under 20%?
        """)

    st.markdown("---")
    st.subheader("Score Scale")
    sc1, sc2, sc3 = st.columns(3)
    sc1.markdown("### 80–100\n**Excellent**\nHealthy habits, good balance.")
    sc2.markdown("### 50–79\n**Needs Work**\nSome areas need attention.")
    sc3.markdown("### 0–49\n**Risky**\nImmediate changes needed!")



# TAB 4 — AI Suggestions

with tabs[3]:
    st.subheader("AI-Based Suggestions")
    st.markdown("Smart, personalised suggestions based on your spending patterns.")

    all_metrics = an.compute_metrics(df)
    suggestions = an.generate_suggestions(all_metrics, df)

    for s in suggestions:
        st.markdown(f'<div class="suggest-box">{s}</div>', unsafe_allow_html=True)



# TAB 5 — Transactions

with tabs[4]:
    st.subheader("All Transactions")

    if df.empty:
        st.info("No transactions yet.")
    else:
        disp = df.copy()
        disp["date"] = disp["date"].dt.strftime("%Y-%m-%d")
        disp["amount"] = disp["amount"].apply(lambda x: f"₹{x:,.2f}")
        disp = disp.rename(columns={"id":"ID","date":"Date","type":"Type","category":"Category","amount":"Amount","note":"Note"})
        st.dataframe(disp, use_container_width=True, hide_index=True)

        st.markdown("---")
        del_id = st.number_input("Enter Transaction ID to delete", min_value=1, step=1)
        if st.button("Delete Transaction"):
            db.delete_transaction(int(del_id))
            st.success(f"Transaction #{del_id} deleted.")
            st.rerun()
