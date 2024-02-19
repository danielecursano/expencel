import datetime
import sqlite3
import pandas as pd

class ISheet:
    def __init__(self, path):
        self.path = path
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cells (date text, desc text, cat text, amount int, author text);")
            conn.commit()
            self.df = pd.read_sql_query("select * from cells", conn)
            self.df = self.df.set_index(pd.to_datetime(self.df.date))

    
    def add_cell(self, desc, cat, amount, author, date):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        values = (date, desc, cat, amount, author)
        cursor.execute("INSERT INTO cells (date, desc, cat, amount, author) VALUES (?, ?, ?, ?, ?)", values)
        conn.commit()
        conn.close()

    def filter(self, start_date=None, end_date=None, author=None, category=None):
        data = self.df
        if start_date and end_date:
            data = data.loc[start_date:end_date]
        if author:
            data = data[data["author"] == author]
        if category:
            data = data[data["cat"] == category]
        return data
    
    @property
    def categories(self):
        return list(set(self.df.cat))
    
    @property
    def authors(self):
        return list(set(self.df.author))
    
    @property 
    def name(self):
        return (self.path.split("/")[-1]).replace(".db","")
    
class Cell:
    def __init__(self, day, desc: str, cat: str, amount: float, author: str):
        self.day = day
        self.desc = desc
        self.cat = cat
        self.amount = amount
        self.author = author

    def __repr__(self) -> str:
        return f"<{self.cat} {self.day} : {self.amount}>"
    
    @property
    def list(self):
        return [self.day, self.cat, self.amount, self.desc, self.author]


def toCell(data):
    return Cell(data[0], data[1], data[2], data[3], data[4])

if __name__=="__main__":
    s = ISheet("db/spese.db")
    t = s.filter(start_date="2024-01-01", end_date="2024-01-31", category="SPESA")
    print(t)
