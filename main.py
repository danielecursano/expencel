from src.server import Server
from src.structs import Sheet
import sys

if __name__=='__main__':
    app = Server()
    debug = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    app.run(debug=debug)
