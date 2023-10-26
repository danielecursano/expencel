import datetime
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

    def __binary_search(self, start, end, low, high):
        if low > high:
            return -1
        middle = (low+high) // 2
        if self.cells[middle].day >= start and self.cells[middle].day <= end:
            return middle
        if self.cells[middle].day < start:
            return self.__binary_search(start, end, middle+1, high)
        else:
            return self.__binary_search(start, end, low, middle-1)

    def range_date(self, start: datetime.date, end: datetime.date):
        '''
        Sperimental method proves that for small range of dates this method is faster than basic_algo
        Execution times closer for bigger timedelta from start and end days
        '''
        filtered_cells = []
        index = self.__binary_search(start, end, 0, len(self.cells))
        left_index = index
        while left_index >= 0 and self.cells[left_index].day >= start:
            filtered_cells.insert(0, self.cells[left_index])
            left_index += -1
        index += 1
        while index < len(self.cells) and self.cells[index].day <= end:
            filtered_cells.append(self.cells[index])
            index += 1
        return filtered_cells
    
    def basic_algo(self, start, end):
        filtered_cells = []
        for i in self.cells:
            if i.day >= start and i.day <= end:
                filtered_cells.append(i)
        return filtered_cells

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
    import time
    #TESTING RANGE DATE METHOD
    s = Sheet.load("2022-2023", "/Users/daniele/Desktop/c++/")
    print(len(s.cells))
    #start_d = s.cells[0].day
    #end_d = s.cells[-1].day
    start_d = datetime.date(2022, 10, 26)
    end_d = datetime.date(2023, 10, 26)
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