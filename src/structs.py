import datetime
from src.constants import DATABASE_PATH
import sqlite3 

class Cell:
    def __init__(self, day: datetime.date, desc: str, cat: str, amount: float, author: str):
        self.day = day
        self.desc = desc
        self.cat = cat
        self.amount = amount
        self.author = author

    def __repr__(self) -> str:
        return f"<{self.cat} {self.day} : {self.amount}>"

class Sheet:
    def __init__(self, name: str, path, loaded=False):
        self.__path = path
        self.name = name
        self.cells = []
        self.authors = []
        self.categories = []
        if not loaded:
            db = sqlite3.connect(self.__path+self.name+".db")
            cursor = db.cursor()
            cursor.execute("CREATE TABLE cells (date text, desc text, cat text, amount int, author text);")
            db.commit()


    def add_cell(self, desc: str, cat: str, amount: int, author: str, day: datetime.date=datetime.date.today()):
        cat = cat.upper()
        author = author.upper()
        if cat not in self.categories:
            self.categories.append(cat)
        if author not in self.authors:
            self.authors.append(author)
        new_cell = Cell(day, desc, cat, amount, author)
        for e in range(0, len(self.cells)):
            if new_cell.day <= self.cells[e].day:
                self.cells.insert(e, new_cell)
                self.__save()
                return
        self.cells.append(new_cell)
        self.__save()

    def filter(self, *filters, cells=None):
        cells_to_filter = self.cells if cells==None else cells
        filtered_cells = []
        if len(filters) == 1 and isinstance(filters[0], int):
            for e in cells_to_filter:
                if e.day.year == filters[0]:
                    filtered_cells.append(e)
        elif len(filters) == 2 and isinstance(filters[0], int) and isinstance(filters[0], int):
            for e in cells_to_filter:
                if e.day.year == filters[0] and e.day.month == filters[1]:
                    filtered_cells.append(e)
        elif len(filters) == 3 and isinstance(filters[0], int) and isinstance(filters[0], int) and isinstance(filters[2], int):
            for e in cells_to_filter:
                if e.day.year == filters[0] and e.day.month == filters[1] and e.day.day == filters[2]:
                    filtered_cells.append(e)
        else:
            if isinstance(filters[0], dict):
                for e in cells_to_filter:
                    tmp = True
                    for k, v in filters[0].items():
                        if k == "category" and v.upper() != e.cat:
                            tmp = False
                        elif k == "author" and v.upper() != e.author:
                            tmp = False
                    if tmp:
                        filtered_cells.append(e)
        return filtered_cells
    
    def __save(self):
        db = sqlite3.connect(self.__path+self.name+".db")
        cursor = db.cursor()
        cursor.execute("DELETE FROM cells")
        for cell in self.cells:
            data = (cell.day, cell.desc, cell.cat, cell.amount, cell.author)
            cursor.execute("INSERT INTO cells VALUES (?, ?, ?, ?, ?)", data)
        db.commit()

    @staticmethod
    def load(name, path):
        new_obj = Sheet(name, path=path, loaded=True)
        db = sqlite3.connect(path+name+".db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM cells")
        data = cursor.fetchall()[::-1]
        for c in data:
            new_obj.add_cell(c[1], c[2], c[3], c[4], datetime.datetime.strptime(c[0], "%Y-%m-%d").date())
        return new_obj
    
        
if __name__=='__main__':
    '''
    s = Sheet("spese")
    s.add_cell("pizza e mozzarella", "uscite", 9, "io", datetime.date(2023, 9, 7))
    s.add_cell("abbonamento atm", "mezzi", 22, "io", datetime.date(2023, 10, 6))
    s.add_cell("pizza e mozzarella", "uscite", 9, "io", datetime.date(2024, 9, 7))
    '''
    s = Sheet.load("spese")