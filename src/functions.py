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

def sum_pd(df):
    return 1, sum(df.amount)

def avg(df):
    return 1, round(sum(df.amount)/df.shape[0], 2)


FUNCTIONS = ["SUM", "AVERAGE", "RECENT", "LESS THAN", "MORE THAN", "SORT", "REVERSED SORT", "PIE", "GRAPH DAY BY DAY", "SUMMARY", "PREDICT"]
FUNCTIONS_HANDLER = {"SUM":sum_pd, "AVG":avg, "PIE": pie}