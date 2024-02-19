from flask import Flask, request, render_template, send_file
from src.interfaces import ISheet
from src.functions import FUNCTIONS_HANDLER
from src.constants import DATABASE_PATH, MONTHS
import datetime 
import json
import os        
import csv

class Server:

    def __init__(self, path=DATABASE_PATH):
        self.sheets = {}
        self.__path = path
        files = os.listdir(path)
        for file in files:
            if file[len(file)-2:] == "db":
                name = file[:len(file)-3]
                self.sheets[name] = ISheet(path+name+".db")
        self.app = Flask(__name__)
        self.app.route("/", methods=["GET"])(self.get_sheet)
        self.app.route("/sheet/<sheet_name>", methods=["GET"])(self.get_cells)
        self.app.route("/add/<sheet_name>", methods=['POST'])(self.add_cell)
        self.app.route("/create/<sheet_name>", methods=['POST'])(self.create_sheet)
        self.app.route("/delete/<sheet_name>", methods=["GET"])(self.delete_sheet)
        self.app.route("/change_path", methods=["POST"])(self.change_path)
        self.app.route("/download/<sheet_name>", methods=["GET"])(self.download_sheet)
        self.app.route("/export/<sheet_name>", methods=["GET"])(self.export_sheet)

    def get_sheet(self, alert=None):
        content = list(self.sheets.keys())
        return render_template("home.html", content=content, msg=alert)
    
    def get_cells(self, sheet_name):
        sheet = self.sheets[sheet_name] if sheet_name in self.sheets.keys() else None
        if not sheet:
            return "Sheet not found"
        args = request.args
        start_date = args.get("start_date")
        function_name = args.get("function")
        end_date = args.get("end_date")
        author = args.get("author") 
        category = args.get("category")
        author = author if author != "Author" else None
        category = category if category != "Category" else None
        content = sheet.filter(author=author, category=category, start_date=start_date, end_date=end_date)
        result = None
        columns = ["Date", "Description", "Category", "Amount", "Author"]
        image = None
        function = FUNCTIONS_HANDLER[function_name.upper()] if function_name else None
        if function:
            tmp, data = function(content)
            if tmp:
                result = data
            else:
                image = "tmp.png"
        return render_template("cells.html", sheet_name=sheet.name, content=content.values.tolist(), function=[function_name if result!=None else None, result], categories=sheet.categories, authors=sheet.authors, functions=FUNCTIONS_HANDLER.keys(), image_path=image, columns=columns)
    
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
        sheet = ISheet(f"src/db/{sheet_name}.db").add_cell(desc, cat, amount, author, date)
        return {"Message": "Success!"}
    
    def create_sheet(self, sheet_name):
        if sheet_name in self.sheets.keys():
            return {"Error:" "Name already used!"}
        new_obj = ISheet(self.__path+sheet_name+".db")
        self.sheets[sheet_name] = new_obj
        return {"Message": "Success!"}
    
    def change_path(self):
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
    
    def export_sheet(self, sheet_name):
        if sheet_name not in self.sheets.keys():
            return self.get_sheet(alert="Sheet not found")
        tmp_sheet = self.sheets[sheet_name]
        with open("src/static/tmp.csv", "w", newline="") as file:
            writer = csv.writer(file)
            field = ["index", "date", "category", "amount", "description", "author"]
            writer.writerow(field)
            for idx in range(0, len(tmp_sheet.cells)):
                tmp = tmp_sheet.cells[idx].list
                tmp.insert(0, idx)
                writer.writerow(tmp)
        return send_file(f"static/tmp.csv", mimetype="text/csv", download_name="sheet.csv", as_attachment=True)

    def run(self, debug=0):
        self.app.run(debug=debug)

if __name__ == "__main__":
    app = Server()
    app.run(1)
