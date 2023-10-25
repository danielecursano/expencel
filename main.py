from src.server import Server
from src.structs import Sheet
import sys

if __name__=='__main__':
    app = Server()
    app.run(debug=1)
