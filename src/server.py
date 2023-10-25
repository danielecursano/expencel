from flask import Flask, request, render_template, send_file
from src.structs import Sheet
import src.functions as functions
from src.constants import DATABASE_PATH
import datetime 
import json
import os

class Server:

    def __init__(self, path=DATABASE_PATH):
        self.sheets = {}
        self.__path = path
        files = os.listdir(path)
        for file in files:
            if file[len(file)-2:] == "db":
                name = file[:len(file)-3]
                self.sheets[name] = Sheet.load(name, path)
        self.app = Flask(__name__)
        self.app.route("/", methods=["GET"])(self.get_sheet)
        self.app.route("/sheet/<sheet_name>", methods=["GET"])(self.get_cells)
        self.app.route("/add/<sheet_name>", methods=['POST'])(self.add_cell)
        self.app.route("/create/", methods=['GET'])(self.create_sheet_form)
        self.app.route("/create/<sheet_name>", methods=['POST'])(self.create_sheet)
        self.app.route("/delete/<sheet_name>", methods=["GET"])(self.delete_sheet)
        self.app.route("/change_path", methods=["GET", "POST"])(self.change_path)
        self.app.route("/download/<sheet_name>", methods=["GET"])(self.download_sheet)

    def get_sheet(self, alert=None):
        content = list(self.sheets.keys())
        return render_template("home.html", content=content, msg=alert)
    
    def create_sheet_form(self):
        return render_template("create_sheet.html")

    def get_cells(self, sheet_name):
        sheet = self.sheets[sheet_name] if sheet_name in self.sheets.keys() else None
        if not sheet:
            return "Sheet not found"
        cells = sheet.cells
        args = request.args
        date = args.get("date")
        if date != None and len(date) > 0:
            date = [int(x) for x in date.split("-")]
        else:
            date = None
        if date:
            day = date[0]
            month = date[1]
            year = date[2]
            if day!=0 and month!=0:
                cells = sheet.filter(year, month, day)
            elif day==0 and month:
                cells = sheet.filter(year, month)
            else:
                cells = sheet.filter(year)
        
        author = args.get("author")
        category = args.get("category")
        filters = {}
        if author and author.upper() in sheet.authors:
            filters["author"] = author
        if category and category.upper() in sheet.categories:
            filters["category"] = category
        cells = sheet.filter(filters, cells=cells) if len(filters.items()) != 0 else cells
        
        content = [[cell.day, cell.cat, cell.desc, cell.amount, cell.author] for cell in cells]

        function = args.get("function")
        image = None
        function = function.upper() if function else None
        if function == "SUM":
            result = functions.SUM(cells)
        elif function == "AVERAGE":
            result = functions.AVERAGE(cells)
        elif function == "RECENT":
            content = functions.RECENT(content)
            result = None
        elif function == "LESS THAN":
            param = int(args.get("param")) if args.get("param") != "" else 10000000
            content = functions.LT(cells, param)
            result = None
        elif function == "MORE THAN":
            param = int(args.get("param")) if args.get("param") != "" else 0
            content = functions.BT(cells, param)
            result = None
        elif function == "SORT":
            content = functions.SORT(cells)
            result = None
        elif function == "REVERSED SORT":
            content = functions.R_SORT(cells)
            result = None
        elif function == "PIE":
            functions.PIE(cells)
            image = "tmp.png"
            result = None
        elif function == "GRAPH DAY BY DAY":
            functions.GRAPH_DAY_BY_DAY(cells)
            image = "tmp.png"
            result = None
        else:
            result = None

        return render_template("cells.html", sheet_name=sheet.name, content=content, function=[function if result!=None else None, result], categories=sheet.categories, authors=sheet.authors, functions=functions.FUNCTIONS, image_path=image)
    
    def add_cell(self, sheet_name):
        sheet = self.sheets[sheet_name] if sheet_name in self.sheets.keys() else None
        if not sheet:
            return {"Error": "Sheet not found!"}
        args = json.loads(request.data)
        date = args["date"]
        cat = args["category"]
        desc = args["description"]
        amount = float(args["amount"])
        author = args["author"]
        sheet.add_cell(desc, cat, amount, author, datetime.datetime.strptime(date, "%d-%m-%Y").date())
        return {"Message": "Success!"}
    
    def create_sheet(self, sheet_name):
        if sheet_name in self.sheets.keys():
            return {"Error": "Sheet already exists!"}
        new_obj = Sheet(sheet_name, self.__path)
        self.sheets[sheet_name] = new_obj
        return {"Message": "Success!"}
    
    def change_path(self):
        if request.method == "GET":
            return render_template("change_path.html")
        args = json.loads(request.data)
        new_path = args["path"]
        self.__path = new_path
        self.sheets = {}
        files = os.listdir(new_path)
        for file in files:
            if file[len(file)-2:] == "db":
                name = file[:len(file)-3]
                self.sheets[name] = Sheet.load(name, new_path)
        return {"Message": "Success!"}
    
    def delete_sheet(self, sheet_name):
        if sheet_name not in self.sheets.keys():
            return self.get_sheet(alert="Sheet not found")
        self.sheets.pop(sheet_name)
        os.remove(self.__path+sheet_name+".db")
        return self.get_sheet(alert="Sheet deleted successfully")
    
    def download_sheet(self, sheet_name):
        if sheet_name not in self.sheets.keys():
            return self.get_sheet(alert="Sheet not found")
        return send_file(f"{self.__path}{sheet_name}.db", attachment_filename=f"{sheet_name}.db")

    def run(self, debug=0):
        self.app.run(debug=debug)

if __name__ == "__main__":
    app = Server()
    app.run(1)
