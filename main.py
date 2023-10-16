from src.server import Server
from src.structs import Sheet
import sys

def main():
    if len(sys.argv) < 2:
        print("Not enough arguments! ex: python main.py path debug")
        return 0
    path = sys.argv[1]
    if path == "None":
        app = Server()
    else:
        app = Server(path)
    debug = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    app.run(debug=debug)

if __name__=='__main__':
    main()
