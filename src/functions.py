def SUM(cells):
    return sum([cell.amount for cell in cells])

def MEAN(cells):
    return SUM(cells)/len(cells)

FUNCTIONS = ["SUM", "MEAN"]