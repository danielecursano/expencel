from flask import Flask, request, render_template, send_file
from src.structs import Sheet
import src.functions as functions
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
                self.sheets[name] = Sheet.load(name, path)
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
        cells = sheet.cells
        args = request.args
        start_date = args.get("start_date")
        end_date = args.get("end_date")

        if start_date not in [None, ""] and end_date not in [None, ""]:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            cells = sheet.range_date(start_date, end_date)
        author = args.get("author")
        category = args.get("category")
        filters = {}
        if author and author.upper() in sheet.authors:
            filters["author"] = author
        if category and category.upper() in sheet.categories:
            filters["category"] = category
        cells = sheet.filter(filters, cells=cells) if len(filters.items()) != 0 else cells
        
        content = [[cell.day, cell.cat, cell.desc, cell.amount, cell.author] for cell in cells]
        columns = ["Date", "Category", "Description", "Amount", "Author"]
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
            result = len(content)
        elif function == "MORE THAN":
            param = int(args.get("param")) if args.get("param") != "" else 0
            content = functions.BT(cells, param)
            result = len(content)
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
        elif function == "SUMMARY":
            content, option = functions.SUMMARY(cells)
            if option == 0:
                columns = ["Category", "Amount"]
            else:
                months = []
                for x in content[0]:
                    months.append(MONTHS[x-1])
                    months.append(f"{MONTHS[x-1]} (%)")
                tmp_total = content[1]["TOTAL"]
                for k, v in content[1].items():
                    if k != "TOTAL":    
                        tmp_len = len(v)
                        added = 0
                        for x in range(0, tmp_len):
                            v.insert(added+x+1, round(100*(v[added+x]/tmp_total[x]), 2))
                            added += 1
                    else:
                        tmp_len = len(v)
                        added = 0
                        for x in range(0, tmp_len):
                            v.insert(added+x+1, 100)
                            added += 1
                content = [[k, *v] for k, v in content[1].items()]
                columns = ["Category"] + months
            result = None
        elif function == "PREDICT":
            content = functions.PREDICT_NEXT_MONTH(cells)
            months = []
            for x in content[0]:
                months.append(MONTHS[(x-1)%12])
                months.append(f"{MONTHS[(x-1)%12]} (%)")
            tmp_total = content[1]["TOTAL"]
            for k, v in content[1].items():
                if k != "TOTAL":    
                    tmp_len = len(v)
                    added = 0
                    for x in range(0, tmp_len):
                        tmp = 0
                        if tmp_total[x] != 0:
                            tmp = round(100*(v[added+x]/tmp_total[x]), 2)
                        v.insert(added+x+1, tmp)
                        added += 1
                else:
                    tmp_len = len(v)
                    added = 0
                    for x in range(0, tmp_len):
                        v.insert(added+x+1, 100)
                        added += 1
            content = [[k, *v] for k, v in content[1].items()]
            columns = ["Category"] + months
            result = None
        else:
            result = None

        return render_template("cells.html", sheet_name=sheet.name, content=content, function=[function if result!=None else None, result], categories=sheet.categories, authors=sheet.authors, functions=functions.FUNCTIONS, image_path=image, columns=columns)
    
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
        sheet.add_cell(desc, cat, amount, author, datetime.datetime.strptime(date, "%Y-%m-%d").date())
        return {"Message": "Success!"}
    
    def create_sheet(self, sheet_name):
        if sheet_name in self.sheets.keys():
            return {"Error:" "Name already used!"}
        new_obj = Sheet(sheet_name, self.__path)
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
