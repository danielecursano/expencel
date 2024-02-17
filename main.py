from src.server import Server
import sys

if __name__=='__main__':
    app = Server()
    app.run(debug=1)
