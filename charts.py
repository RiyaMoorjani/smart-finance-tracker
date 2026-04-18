import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

PALETTE = ["#4CAF50", "#2196F3", "#FF9800", "#E91E63", "#9C27B0",
           "#00BCD4", "#FF5722", "#607D8B", "#795548", "#FFC107"]

def pie_chart(cat_totals, title="Expense Breakdown"):
    if not cat_totals:
        return None
    fig, ax = plt.subplots(figsize=(6, 4))
    labels = [k.title() for k in cat_totals.keys()]
    sizes  = list(cat_totals.values())
    colors = PALETTE[:len(sizes)]
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors,
        autopct="%1.1f%%", startangle=140,
        textprops={"fontsize": 9}
    )
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    fig.tight_layout()
    return fig

def bar_chart(df, year, month):
    """Monthly income vs expense bar."""
    months = []
    incomes = []
    expenses = []
    for m in range(1, 13):
        sub = df[
            (pd.to_datetime(df["date"]).dt.year == int(year)) &
            (pd.to_datetime(df["date"]).dt.month == m)
        ]
        inc = sub[sub["type"] == "income"]["amount"].sum()
        exp = sub[sub["type"] == "expense"]["amount"].sum()
        months.append(pd.Timestamp(year=int(year), month=m, day=1).strftime("%b"))
        incomes.append(inc)
        expenses.append(exp)

    x = np.arange(12)
    w = 0.35
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(x - w/2, incomes,  w, label="Income",  color="#4CAF50", alpha=0.85)
    ax.bar(x + w/2, expenses, w, label="Expense", color="#F44336", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=9)
    ax.set_ylabel("₹ Amount")
    ax.set_title(f"Income vs Expense — {year}", fontsize=12, fontweight="bold")
    ax.legend()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"₹{v:,.0f}"))
    fig.tight_layout()
    return fig

def health_gauge(score):
    """Draw a simple semicircle gauge for the health score."""
    fig, ax = plt.subplots(figsize=(4, 2.5))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.1, 1.2)
    ax.axis("off")

    # background arc
    theta = np.linspace(np.pi, 0, 200)
    ax.plot(np.cos(theta), np.sin(theta), color="#e0e0e0", linewidth=18, solid_capstyle="round")

    # colored arc up to score
    color = "#4CAF50" if score >= 80 else "#FF9800" if score >= 50 else "#F44336"
    frac  = score / 100
    theta2 = np.linspace(np.pi, np.pi - frac * np.pi, 200)
    ax.plot(np.cos(theta2), np.sin(theta2), color=color, linewidth=18, solid_capstyle="round")

    ax.text(0, 0.25, f"{score}", ha="center", va="center", fontsize=28, fontweight="bold", color=color)
    label = "Excellent" if score >= 80 else "Needs Work" if score >= 50 else "Risky"
    ax.text(0, -0.05, label, ha="center", va="center", fontsize=11, color=color)
    ax.set_title("Financial Health Score", fontsize=11, fontweight="bold", pad=4)
    fig.tight_layout()
    return fig

def pillar_bar(pillars):
    """Horizontal bar for each score pillar."""
    fig, ax = plt.subplots(figsize=(5, 3))
    names  = list(pillars.keys())
    values = list(pillars.values())
    colors = ["#4CAF50" if v >= 20 else "#FF9800" if v >= 12 else "#F44336" for v in values]
    bars = ax.barh(names, values, color=colors, height=0.5)
    ax.set_xlim(0, 25)
    ax.set_xlabel("Score (max 25)")
    ax.set_title("Score Breakdown", fontsize=11, fontweight="bold")
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{val}", va="center", fontsize=9, fontweight="bold")
    fig.tight_layout()
    return fig

def category_trend(df, category):
    """Line chart: monthly spend for one category."""
    df2 = df[df["category"].str.lower() == category.lower()].copy()
    if df2.empty:
        return None
    df2["month"] = pd.to_datetime(df2["date"]).dt.to_period("M")
    monthly = df2.groupby("month")["amount"].sum().reset_index()
    monthly["month"] = monthly["month"].astype(str)
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(monthly["month"], monthly["amount"], marker="o", color="#2196F3", linewidth=2)
    ax.fill_between(monthly["month"], monthly["amount"], alpha=0.15, color="#2196F3")
    ax.set_title(f"Monthly Trend — {category.title()}", fontsize=11, fontweight="bold")
    ax.set_ylabel("₹ Amount")
    ax.tick_params(axis="x", rotation=30, labelsize=8)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"₹{v:,.0f}"))
    fig.tight_layout()
    return fig
