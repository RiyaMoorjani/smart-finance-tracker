import numpy as np
import pandas as pd

# ── Category buckets ─────────────────────────────────────────────────────────
ESSENTIAL_CATS    = ["food", "rent", "utilities", "healthcare", "transport"]
INVESTMENT_CATS   = ["stocks", "mutual funds", "fd", "crypto", "investment"]
NON_ESSENTIAL_CATS = ["shopping", "entertainment", "dining out", "travel", "subscriptions", "other"]

def classify_category(cat):
    cat = cat.lower()
    if cat in ESSENTIAL_CATS:    return "essential"
    if cat in INVESTMENT_CATS:   return "investment"
    return "non_essential"


# ── Core metrics ─────────────────────────────────────────────────────────────
def compute_metrics(df):
    """Return a dict of key financial metrics from a transactions DataFrame."""
    if df.empty:
        return {}

    income_df  = df[df["type"] == "income"]
    expense_df = df[df["type"] == "expense"]

    total_income  = income_df["amount"].sum()
    total_expense = expense_df["amount"].sum()

    # category-level breakdown
    cat_totals = expense_df.groupby("category")["amount"].sum().to_dict()

    essential_spend   = sum(v for k, v in cat_totals.items() if classify_category(k) == "essential")
    investment_spend  = sum(v for k, v in cat_totals.items() if classify_category(k) == "investment")
    non_ess_spend     = sum(v for k, v in cat_totals.items() if classify_category(k) == "non_essential")

    savings = total_income - total_expense
    savings_rate      = (savings / total_income * 100)          if total_income else 0
    investment_rate   = (investment_spend / total_income * 100) if total_income else 0
    food_pct          = (cat_totals.get("food", 0) / total_income * 100) if total_income else 0
    non_ess_rate      = (non_ess_spend / total_income * 100)    if total_income else 0
    essential_rate    = (essential_spend / total_income * 100)  if total_income else 0

    return {
        "total_income":      total_income,
        "total_expense":     total_expense,
        "savings":           savings,
        "savings_rate":      round(savings_rate, 1),
        "investment_rate":   round(investment_rate, 1),
        "food_pct":          round(food_pct, 1),
        "non_ess_rate":      round(non_ess_rate, 1),
        "essential_rate":    round(essential_rate, 1),
        "cat_totals":        cat_totals,
        "essential_spend":   essential_spend,
        "investment_spend":  investment_spend,
        "non_ess_spend":     non_ess_spend,
    }


# ── Financial Health Score (0-100) ───────────────────────────────────────────
def compute_health_score(metrics):
    """
    Weighted score from 4 pillars (each 0-25):
      1. Savings rate      (target ≥ 20 %)
      2. Investment rate   (target 10-30 %)
      3. Essential ratio   (target ≤ 50 %)
      4. Non-essential     (target ≤ 20 %)
    """
    if not metrics:
        return 0, {}

    sr   = metrics["savings_rate"]
    ir   = metrics["investment_rate"]
    er   = metrics["essential_rate"]
    nr   = metrics["non_ess_rate"]

    # pillar 1 – savings (0–25)
    s1 = min(25, (sr / 20) * 25) if sr >= 0 else 0

    # pillar 2 – investment (0–25): sweet spot 10–30 %
    if   ir < 10:   s2 = (ir / 10) * 15          # too low
    elif ir <= 30:  s2 = 25                        # ideal
    else:           s2 = max(0, 25 - (ir - 30))   # too high → penalty

    # pillar 3 – essential spending (0–25)
    s3 = 25 if er <= 50 else max(0, 25 - (er - 50) * 0.5)

    # pillar 4 – non-essential spending (0–25)
    s4 = 25 if nr <= 20 else max(0, 25 - (nr - 20) * 0.8)

    score = round(s1 + s2 + s3 + s4)
    pillars = {
        "Savings Rate":     round(s1, 1),
        "Investment Mix":   round(s2, 1),
        "Essential Spend":  round(s3, 1),
        "Discretionary":    round(s4, 1),
    }
    return score, pillars


# ── Behavior judgements ──────────────────────────────────────────────────────
def spending_judgements(metrics):
    """Return list of (emoji, message, severity) tuples."""
    if not metrics:
        return []

    judgements = []
    sr  = metrics["savings_rate"]
    ir  = metrics["investment_rate"]
    fp  = metrics["food_pct"]
    nr  = metrics["non_ess_rate"]

    # Savings
    if sr >= 30:
        judgements.append(("", f"Savings rate is {sr}% — excellent discipline!", "good"))
    elif sr >= 20:
        judgements.append(("", f"Savings rate is {sr}% — decent, aim for 20–30%.", "ok"))
    elif sr >= 0:
        judgements.append(("", f"Savings rate is only {sr}% — dangerously low. Target ≥ 20%.", "bad"))
    else:
        judgements.append(("", f"You are spending MORE than you earn! Deficit: {abs(sr):.1f}%.", "critical"))

    # Investment
    if ir == 0:
        judgements.append(("", "No investments recorded. Consider allocating 10–30% of income.", "info"))
    elif ir <= 10:
        judgements.append(("", f"Investment at {ir}% — slightly low. Aim for 10–30%.", "ok"))
    elif ir <= 30:
        judgements.append(("", f"Investment rate {ir}% — well balanced!", "good"))
    elif ir <= 40:
        judgements.append(("", f"Investment is {ir}% — high risk zone. Keep below 30%.", "bad"))
    else:
        judgements.append(("", f"Investment at {ir}%! Extremely risky. Reduce & build emergency fund first.", "critical"))

    # Food
    if fp > 35:
        judgements.append(("", f"Food spending is {fp}% of income — too high. Try meal planning.", "bad"))
    elif fp > 20:
        judgements.append(("", f"Food at {fp}% — moderate. Small savings possible.", "ok"))

    # Non-essential
    if nr > 30:
        judgements.append(("", f"Discretionary spending is {nr}% — trim lifestyle expenses.", "bad"))
    elif nr > 20:
        judgements.append(("", f"Discretionary at {nr}% — slightly above the 20% guideline.", "ok"))

    return judgements


# ── AI Suggestions (rule-based + ML anomaly hint) ───────────────────────────
def generate_suggestions(metrics, df):
    """Return list of actionable suggestion strings."""
    if not metrics:
        return []

    suggestions = []
    sr  = metrics["savings_rate"]
    ir  = metrics["investment_rate"]
    inc = metrics["total_income"]
    cats = metrics["cat_totals"]

    # Emergency fund check
    monthly_expense = metrics["total_expense"]
    if monthly_expense > 0 and metrics["savings"] < monthly_expense * 3:
        target = round(monthly_expense * 3)
        suggestions.append(f"Build an emergency fund of ₹{target:,} (3 months of expenses) before increasing investments.")

    # Savings boost
    if sr < 20 and inc > 0:
        needed = round(inc * 0.20 - metrics["savings"])
        suggestions.append(f"Cut ₹{needed:,}/month from expenses to reach a healthy 20% savings rate.")

    # Investment re-balancing
    if ir > 30:
        excess = round((ir - 25) / 100 * inc)
        suggestions.append(f"Reduce stock/investment by ₹{excess:,} and move it to savings or FD for safety.")
    if ir > 0 and ir <= 30:
        # Diversification nudge
        if cats.get("stocks", 0) > 0 and cats.get("mutual funds", 0) == 0 and cats.get("fd", 0) == 0:
            suggestions.append("All investments are in stocks. Diversify: add Mutual Funds or FD to reduce risk.")

    # Top 2 discretionary categories to cut
    non_ess_cats = {k: v for k, v in cats.items() if classify_category(k) == "non_essential"}
    top2 = sorted(non_ess_cats.items(), key=lambda x: x[1], reverse=True)[:2]
    for cat, amt in top2:
        cut = round(amt * 0.20)
        if cut >= 200:
            suggestions.append(f" Reduce '{cat.title()}' spending by ₹{cut:,}/month — that's ₹{cut*12:,} saved per year!")

    # Simple ML: flag if any category spending is unusually high (z-score)
    if len(df) >= 5:
        exp_df = df[df["type"] == "expense"].copy()
        if not exp_df.empty:
            cat_monthly = exp_df.groupby("category")["amount"].sum()
            if len(cat_monthly) >= 3:
                vals = cat_monthly.values
                min_val = vals.min()
                max_val = vals.max()
                scaled = (vals - min_val) / (max_val - min_val) if max_val > min_val else vals
                for i, (cat, s) in enumerate(zip(cat_monthly.index, scaled)):
                    if s > 0.85:
                        suggestions.append(f"ML Alert: '{cat.title()}' is your highest spend category — review if it aligns with your goals.")
                        break  # one ML alert is enough

    if not suggestions:
        suggestions.append("Your finances look healthy! Keep maintaining this balance.")

    return suggestions
