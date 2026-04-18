# 💰 Smart Finance Tracker

A Python + Streamlit personal finance app with AI-powered spending analysis, financial health scoring, and smart investment advice.

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Load demo data
```bash
python seed_data.py
```

### 3. Launch the app
```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

## 📁 Project Structure

```
finance_tracker/
│
├── app.py           ← Main Streamlit UI (5 tabs)
├── database.py      ← SQLite CRUD operations
├── analysis.py      ← Metrics, Health Score, Judgements, AI Suggestions (scikit-learn)
├── charts.py        ← Matplotlib charts (pie, bar, gauge, trend)
├── seed_data.py     ← Demo data loader
├── requirements.txt
└── finance.db       ← Auto-created SQLite database
```

---

## 🧠 Features

| Feature | Description |
|---|---|
| **Expense Tracking** | Add income & expenses with category, date, notes |
| **Monthly Summary** | View income vs expense by month |
| **Spending Analysis** | Behaviour judgements: "Food is 35% → too high" |
| **Health Score** | 0–100 score across 4 financial pillars |
| **AI Suggestions** | Rule-based + ML anomaly detection for personalised tips |
| **Investment Education** | Teaches risk management, diversification |

---

## 📊 Tech Stack

- **UI**: Streamlit
- **Data**: Pandas, NumPy, SQLite
- **Charts**: Matplotlib
- **Intelligence**: scikit-learn (MinMaxScaler for anomaly detection)

---

## 🎯 Financial Score Pillars (0–25 each)

1. **Savings Rate** — Target ≥ 20% of income  
2. **Investment Mix** — Target 10–30% (sweet spot)  
3. **Essential Spend** — Target ≤ 50% of income  
4. **Discretionary** — Target ≤ 20% of income  

**80+** → Excellent | **50–79** → Needs Work | **<50** → Risky
