def SUM(cells):
    return sum([cell.amount for cell in cells])

def MEAN(cells):
    return SUM(cells)/len(cells)

def RECENT(cells):
    return cells[::-1]

FUNCTIONS = ["SUM", "MEAN", "RECENT"]