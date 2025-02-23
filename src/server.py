from flask import Flask, request, render_template, send_file
from src.interfaces import ISheet
from src.functions import FUNCTIONS_HANDLER
from src.constants import DATABASE_PATH
import datetime 
import json
import os        
import csv
from src.agent import interact

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
        columns = ["Date", "Description", "Category", "Amount", "Author"]

        args = request.args
        start_date = args.get("start_date")
        function_name = args.get("function")
        end_date = args.get("end_date")
        author = args.get("author") 
        category = args.get("category")
        prompt = args.get("prompt")

        #print(bool(prompt))

        author = author if author != "Author" else None
        category = category if category != "Category" else None
        function_name = function_name if function_name not in ["", None, "Function"] else None

        content = sheet.filter(author=author, category=category, start_date=start_date, end_date=end_date)

        result = None
        image = None

        function = FUNCTIONS_HANDLER[function_name.upper()] if function_name else None
        if function:
            type, data = function(content)
            if type == 0:
                image = "tmp.png"
            elif type == 1:
                result = data
            elif type == 2:
                content = data
            elif type == 3:
                content = data
                columns = ["Category"] + list(data.index)
                content = content.T
                content["cat"] = content.index
                column = content.pop("cat")
                content.insert(0, "cat", column)

        llm_response = None
        if prompt:
            llm_response = interact(sheet_name, prompt, content)
            self.sheets[sheet_name] = ISheet(f"src/db/{sheet_name}.db")
            llm_response = llm_response.content

        return render_template("cells.html",sheet_name=sheet.name, llm_response=llm_response, content=content.values.tolist(), function=[function_name if result!=None else None, result], categories=sheet.categories, authors=sheet.authors, functions=FUNCTIONS_HANDLER.keys(), image_path=image, columns=columns)
    
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
        self.sheets[sheet_name] = ISheet(f"src/db/{sheet_name}.db")
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
                self.sheets[name] = ISheet.load(name, new_path)
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
        return send_file(f"db/{sheet_name}.db", attachment_filename=f"{sheet_name}.db")
    
    def export_sheet(self, sheet_name):
        sheet = self.sheets[sheet_name] if sheet_name in self.sheets.keys() else None
        if not sheet:
            return self.get_sheet(alert="Sheet not found")
        content = sheet.filter()
        content.to_csv("src/static/tmp.csv", sep=",", index=False, encoding="utf-8")
        return send_file(f"static/tmp.csv", mimetype="text/csv", download_name="sheet.csv", as_attachment=True)

    def run(self, debug=0):
        self.app.run(debug=debug)

if __name__ == "__main__":
    app = Server()
    app.run(1)
