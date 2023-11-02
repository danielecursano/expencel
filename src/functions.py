import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')

def SUM(cells):
    return sum([cell.amount for cell in cells])

def AVERAGE(cells):
    return SUM(cells)/len(cells)

def RECENT(cells):
    return cells[::-1]

def LT(cells, param):
    tmp = [cell if cell.amount <= param else None for cell in cells]
    return [[cell.day, cell.cat, cell.desc, cell.amount, cell.author] for cell in tmp if cell is not None]

def BT(cells, param):
    tmp = [cell if cell.amount >= param else None for cell in cells]
    return [[cell.day, cell.cat, cell.desc, cell.amount, cell.author] for cell in tmp if cell is not None]

def SORT(cells):
    cells.sort(key=lambda cell: cell.amount, reverse=True)
    return [[cell.day, cell.cat, cell.desc, cell.amount, cell.author] for cell in cells]

def R_SORT(cells):
    return SORT(cells)[::-1]

def PIE(cells):
    data = {}
    total = 0
    for c in cells:
        if c.cat not in data:
            data[c.cat] = 0
        data[c.cat] += c.amount
        total += c.amount

    def absolute_value(val):
        a  = round(val/100.*total, 2)
        return f"€{a}"
    
    fig, ax = plt.subplots()
    ax.pie(list(data.values()), labels=list(data.keys()), autopct=absolute_value)
    plt.savefig("src/static/tmp.png")
    return 0

def GRAPH_DAY_BY_DAY(cells):
    from datetime import timedelta
    delta_data = (cells[-1].day-cells[0].day).days
    days = [cells[0].day + timedelta(i) for i in range(0, delta_data+1)]
    data = [0 for x in range(0, len(days))]
    for cell in cells:
        data[days.index(cell.day)] += cell.amount
    fix, ax = plt.subplots()
    labels = [days[x] for x in range(0, len(days)) if data[x] != 0 ]
    ax.plot(days, data)
    ax.set_xticks(labels)
    ax.tick_params(axis='x', labelrotation=10, labelsize=8) 
    plt.savefig("src/static/tmp.png")
    return 0

def SUMMARY_MONTHS(cells):
    min_month = cells[0].day.month
    max_month = cells[-1].day.month
    months = []
    rows = {"TOTAL": [0]*(max_month-min_month+1)}
    for cell in cells:
        tmp_cat = cell.cat
        tmp_month = cell.day.month
        if tmp_month not in months:
            months.append(tmp_month)
        if tmp_cat not in rows.keys():
            rows[tmp_cat] = [0]*(max_month-min_month+1)
        rows[tmp_cat][tmp_month-min_month] += cell.amount
        rows["TOTAL"][tmp_month-min_month] += cell.amount
    filtered_row = {key: value for key, value in rows.items() if key != "TOTAL"}
    filtered_row["TOTAL"] = rows["TOTAL"]
    return [months, filtered_row], 1

def SUMMARY(cells):
    if (cells[-1].day - cells[0].day).days >= 31:
        return SUMMARY_MONTHS(cells)
    tmp = {}
    for cell in cells:
        if cell.cat not in tmp.keys():
            tmp[cell.cat] = 0
        tmp[cell.cat] += cell.amount
    tmp["TOTAL"] = sum([x for x in tmp.values()])
    return [[k, v] for k, v in tmp.items()], 0

FUNCTIONS = ["SUM", "AVERAGE", "RECENT", "LESS THAN", "MORE THAN", "SORT", "REVERSED SORT", "PIE", "GRAPH DAY BY DAY", "SUMMARY"]