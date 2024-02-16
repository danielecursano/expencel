import datetime
import sqlite3 

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
                return
        self.cells.append(new_cell)

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
    import time
    #TESTING RANGE DATE METHOD
    s = Sheet.load("2022-2023", "/Users/daniele/Desktop/c++/")
    print(len(s.cells))
    start_d = s.cells[0].day
    end_d = s.cells[-1].day
    #start_d = datetime.date(2022, 10, 26)
    #end_d = datetime.date(2023, 10, 26)
    start = time.time()
    tmp = s.range_date(start_d, end_d)
    end = time.time()
    print(f"binary search time: {end-start}")
    start = time.time()
    tmp2 = s.basic_algo(start_d, end_d)
    end = time.time()
    print(f"basic algo: {end-start}")
    print(tmp==tmp2)
    '''
    for i in range(500):
        d = datetime.date(2023, 1, 1) + datetime.timedelta(i)
        s.add_cell("test", "test", 1, "io", d)
    '''