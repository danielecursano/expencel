from flask import Flask, request, render_template
from src.structs import Sheet
import src.functions as functions
from src.constants import DATABASE_PATH
import datetime 
import json
import os

class Server:

    def __init__(self, folder=DATABASE_PATH):
        self.sheets = {}
        files = os.listdir(folder)
        for file in files:
            name = file[:len(file)-3]
            self.sheets[name] = Sheet.load(name)
        self.app = Flask(__name__)
        self.app.route("/", methods=["GET"])(self.get_sheet)
        self.app.route("/sheet/<sheet_name>", methods=["GET"])(self.get_cells)
        self.app.route("/add/<sheet_name>", methods=['POST'])(self.add_cell)
        self.app.route("/create/<sheet_name>", methods=['POST'])(self.create_sheet)
        self.app.route("/delete/<sheet_name>", methods=["GET"])(self.delete_sheet)

    def get_sheet(self, alert=None):
        content = list(self.sheets.keys())
        return render_template("home.html", content=content, msg=alert)

    def get_cells(self, sheet_name):
        sheet = self.sheets[sheet_name] if sheet_name in self.sheets.keys() else None
        if not sheet:
            return "Sheet not found"

        cells = sheet.cells
        args = request.args
        date = args.get("date")
        date = [int(x) for x in list(date)] if (date != None or date == "") else 0
        if date and len(date)==8:
            day = date[0]*10 + date[1]
            month = date[2]*10 + date[3]
            year = date[4]*1000 + date[5]*100 + date[6]*10 + date[7]
            if day and month:
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
        function = function.upper() if function else None
        if function == "SUM":
            result = functions.SUM(cells)
        elif function == "AVERAGE":
            result = functions.MEAN(cells)
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
        else:
            result = None

        return render_template("cells.html", sheet_name=sheet.name, content=content, function=[function if result!=None else None, result], categories=sheet.categories, authors=sheet.authors, functions=functions.FUNCTIONS)
    
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
        new_obj = Sheet(sheet_name)
        self.sheets[sheet_name] = new_obj
        return {"Message": "Success!"}
    
    def delete_sheet(self, sheet_name):
        if sheet_name not in self.sheets.keys():
            return self.get_sheet(alert="Sheet not found")
        self.sheets.pop(sheet_name)
        os.remove(DATABASE_PATH+sheet_name+".db")
        return self.get_sheet(alert="Sheet deleted successfully")

    def run(self, debug=0):
        self.app.run(debug=debug)

if __name__ == "__main__":
    app = Server()
    app.run(1)
