import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
matplotlib.use('agg')

def pie(df):
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    grouped_df = df.groupby('cat')['amount'].sum()
    total = sum(grouped_df)/100
    pie_chart = grouped_df.plot(kind="pie", figsize=(6, 6), legend=False, autopct=lambda x: f'€{x*total:.2f}')
    pie_chart.set_ylabel('')  
    fig = pie_chart.get_figure()
    fig.savefig("src/static/tmp.png")
    plt.close(fig) 
    return 0, 0

def plot_months(df):
    monthly_expenses = df.groupby(df["date"].dt.to_period("M"))['amount'].sum()
    monthly_expenses.plot(kind="line", figsize=(10, 6))
    plt.xlabel("Month")
    plt.ylabel("Total Expenses")
    plt.title("Monthly Expenses")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.savefig("src/static/tmp.png")
    plt.close() 
    return 0, 0

def sum_pd(df):
    return 1, sum(df.amount)

def avg(df):
    return 1, round(sum(df.amount)/df.shape[0], 2)

def recent(df):
    return 2, df.sort_index(ascending=False)

def sortByValueAsc(df):
    return 2, df.sort_values(by="amount")

def sortByValueDesc(df):
    return 2, df.sort_values(by="amount", ascending=False)

def summary(df):
    new_df = df.groupby([df["date"].dt.to_period("M"), 'cat'])["amount"].sum().unstack()
    new_df.fillna(0, inplace=True)
    new_df["TOTAL"] = df.groupby([df["date"].dt.to_period("M")])["amount"].sum()
    return 3, new_df

def groupbyCat(df):
    df = df.groupby("cat")["amount"].sum().reset_index(name="total_expenses")
    df.fillna(0, inplace=True)
    total_row = df
    return 3, df

FUNCTIONS_HANDLER = {"SUM":sum_pd, "AVG":avg, "PIE": pie, "RECENT": recent, "SORT ASC": sortByValueAsc, "SORT DESC": sortByValueDesc, "PLOT LINE": plot_months, "SUMMARY": summary, "GROUP_BY_CAT": groupbyCat}