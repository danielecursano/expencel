from src.server import Server
from src.structs import Sheet

if __name__=='__main__':
    s = Sheet.load("spese")
    app = Server(s)
    app.run(debug=1)