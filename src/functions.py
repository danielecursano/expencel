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

FUNCTIONS = ["SUM", "AVERAGE", "RECENT", "LESS THAN", "MORE THAN", "SORT", "REVERSED SORT"]