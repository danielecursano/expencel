import datetime
import sqlite3
from src.structs import Cell

class ISheet:
    def __init__(self, path):
        self.path = path
    
    def add_cell(self, desc, cat, amount, author, date):
        print("adding cells")
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        values = (date, desc, cat, amount, author)
        cursor.execute("INSERT INTO cells (date, desc, cat, amount, author) VALUES (?, ?, ?, ?, ?)", values)
        conn.commit()
        conn.close()

    def filter(self, start_date=None, end_date=None, author=None, category=None):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        query = "SELECT * FROM cells WHERE 1=1"
        params = []

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        if author:
            query += " AND author = ?"
            params.append(author)
        if category:
            query += " AND cat = ?"
            params.append(category)

        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()
        return data
    
def toCell(data):
    return Cell(data[0], data[1], data[2], data[3], data[4])

if __name__=="__main__":
    s = ISheet("db/spese.db")
    t = s.filter(start_date="2024-01-01", end_date="2024-01-31", category="SPESA")
    print(t)
